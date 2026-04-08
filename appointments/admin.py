from django.contrib import admin
<<<<<<< HEAD
from .models import Appointment, Doctor, DoctorSchedule

class DoctorScheduleInline(admin.TabularInline):
    model = DoctorSchedule
    extra = 1
    fields = ('day', 'start_time', 'end_time', 'notes')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')
    search_fields = ('name', 'specialty')
    list_filter = ('specialty',)
    inlines = [DoctorScheduleInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'specialty', 'experience', 'details', 'highlights', 'image_url')
        }),
    )

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'start_time', 'end_time', 'notes')
    list_filter = ('day', 'doctor')
    search_fields = ('doctor__name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'created_at')
    search_fields = ('fullname', 'phone')
=======
from .models import Appointment # Hoặc tên Model bạn đã đặt

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'created_at') # Hiện các cột này ra danh sách
    search_fields = ('fullname', 'phone') # Cho phép tìm kiếm theo tên hoặc số ĐT
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
