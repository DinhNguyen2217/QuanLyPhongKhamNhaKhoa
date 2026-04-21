from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from apps.accounts.models import User
from apps.appointments.models import Appointment
from apps.catalog.models import  Service
from apps.doctors.models import Doctor, DoctorSchedule
from .forms import SHIFTS, WEEKDAYS, ServiceScheduleBulkForm


@staff_member_required
def dashboard_home_view(request):
    context = {
        'user_count': User.objects.filter(role='customer').count(),
        'doctor_count': Doctor.objects.count(),
        'service_count': Service.objects.count(),
        
        'appointment_count': Appointment.objects.count(),
        'latest_appointments': Appointment.objects.select_related('doctor__user', 'service').all()[:10],
        'doctor_cards': Doctor.objects.select_related('user').prefetch_related('services').all()[:6],
    }
    return render(request, 'dashboard/home.html', context)


@staff_member_required
def doctor_schedule_manage_view(request):
    services = Service.objects.prefetch_related('doctors').all()
    selected_service = None
    initial = {}

    service_id = request.POST.get('service') or request.GET.get('service')
    if service_id:
        try:
            selected_service = services.get(pk=service_id)
            sample_doctor = selected_service.doctors.first()
            if sample_doctor:
                initial['weekdays'] = [str(item.weekday) for item in sample_doctor.schedules.filter(is_active=True)]
                initial['shifts'] = list({item.shift for item in sample_doctor.schedules.filter(is_active=True)})
        except Service.DoesNotExist:
            selected_service = None

    if request.method == 'POST':
        form = ServiceScheduleBulkForm(request.POST)
        if form.is_valid():
            service = form.cleaned_data['service']
            weekdays = [int(item) for item in form.cleaned_data['weekdays']]
            shifts = form.cleaned_data['shifts']
            doctors = service.doctors.all()
            for doctor in doctors:
                doctor.schedules.all().delete()
                for weekday in weekdays:
                    for shift in shifts:
                        DoctorSchedule.objects.create(doctor=doctor, weekday=weekday, shift=shift, is_active=True)
            messages.success(request, f'Đã cập nhật lịch làm việc theo khoa/dịch vụ: {service.name}.')
            return redirect(f"/dashboard/doctor-schedule/?service={service.pk}")
    else:
        form = ServiceScheduleBulkForm(initial={'service': service_id, **initial})

    preview_rows = []
    if selected_service:
        for doctor in selected_service.doctors.select_related('user'):
            items = doctor.schedules.filter(is_active=True)
            preview_rows.append({'doctor': doctor, 'items': items})

    return render(request, 'dashboard/doctor_schedule_manage.html', {
        'form': form,
        'services': services,
        'selected_service': selected_service,
        'preview_rows': preview_rows,
        'weekdays': dict(WEEKDAYS),
        'shifts': dict(SHIFTS),
    })
