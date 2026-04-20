from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .forms import AdminBulkDoctorScheduleForm
from .models import Doctor, DoctorSchedule


class DoctorScheduleInline(admin.TabularInline):
    model = DoctorSchedule
    extra = 0
    verbose_name = 'Ca làm việc'
    verbose_name_plural = 'Lịch làm việc hiện tại'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department_list', 'position', 'qualification', 'years_of_experience', 'schedule_count')
    search_fields = ('full_name', 'user__username', 'user__first_name', 'user__last_name', 'position', 'qualification', 'services__name')
    filter_horizontal = ('services',)
    list_filter = ('position', 'services')
    inlines = [DoctorScheduleInline]
    fieldsets = (
        ('Tài khoản liên kết', {'fields': ('user',)}),
        ('Thông tin chính', {'fields': ('full_name', 'avatar', 'position', 'qualification', 'years_of_experience', 'age')}),
        ('Dịch vụ phụ trách', {'fields': ('services',)}),
        ('Giới thiệu', {'fields': ('achievement', 'bio')}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('services', 'schedules')

    @admin.display(description='Dịch vụ phụ trách')
    def department_list(self, obj):
        return ', '.join(obj.services.values_list('name', flat=True)) or 'Chưa gán'

    @admin.display(description='Số ca đã xếp')
    def schedule_count(self, obj):
        return obj.schedules.filter(is_active=True).count()


@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'service_list', 'get_weekday_display', 'get_shift_display', 'is_active')
    list_filter = ('weekday', 'shift', 'is_active', 'doctor__services')
    search_fields = ('doctor__full_name', 'doctor__user__username', 'doctor__services__name')
    change_list_template = 'admin/doctors/doctorschedule/change_list.html'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('doctor', 'doctor__user').prefetch_related('doctor__services')

    @admin.display(description='Dịch vụ phụ trách')
    def service_list(self, obj):
        return ', '.join(obj.doctor.services.values_list('name', flat=True)) or 'Chưa gán'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk-add/', self.admin_site.admin_view(self.bulk_add_view), name='doctors_doctorschedule_bulk_add'),
        ]
        return custom_urls + urls

    def add_view(self, request, form_url='', extra_context=None):
        return HttpResponseRedirect(reverse('admin:doctors_doctorschedule_bulk_add'))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        doctors = Doctor.objects.prefetch_related('schedules', 'services').order_by('full_name')
        rows = []
        for doctor in doctors:
            active_items = doctor.schedules.filter(is_active=True).order_by('weekday', 'shift')
            rows.append({
                'doctor': doctor,
                'services': doctor.services.all(),
                'count': active_items.count(),
                'items': active_items,
            })
        extra_context['schedule_matrix'] = rows
        extra_context['bulk_add_url'] = reverse('admin:doctors_doctorschedule_bulk_add')
        return super().changelist_view(request, extra_context=extra_context)

    def bulk_add_view(self, request):
        form = AdminBulkDoctorScheduleForm(request.POST or None)
        context = {
            **self.admin_site.each_context(request),
            'opts': self.model._meta,
            'title': 'Xếp lịch cho từng bác sĩ',
            'form': form,
        }
        if request.method == 'POST' and form.is_valid():
            doctor = form.cleaned_data['doctor']
            weekdays = [int(value) for value in form.cleaned_data['weekdays']]
            shifts = list(form.cleaned_data['shifts'])
            replace_existing = form.cleaned_data['replace_existing']

            qs = doctor.schedules.filter(is_active=True)
            removed = 0
            if replace_existing:
                removed = qs.count()
                qs.delete()
            created = 0
            for weekday in weekdays:
                for shift in shifts:
                    _, was_created = DoctorSchedule.objects.get_or_create(
                        doctor=doctor,
                        weekday=weekday,
                        shift=shift,
                        defaults={'is_active': True},
                    )
                    created += int(was_created)
            messages.success(
                request,
                f'Đã cập nhật lịch cho bác sĩ {doctor.display_name}. Tạo mới {created} ca làm việc'
                + (f', xóa {removed} lịch cũ.' if replace_existing else '.'),
            )
            return HttpResponseRedirect(reverse('admin:doctors_doctorschedule_changelist'))
        return TemplateResponse(request, 'admin/doctors/doctorschedule/bulk_add.html', context)
