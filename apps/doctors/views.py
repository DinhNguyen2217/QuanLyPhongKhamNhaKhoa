from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from common.choices import (
    ROLE_DOCTOR,
    SHIFT_CHOICES,
    WEEKDAY_CHOICES,
    APPOINTMENT_CONFIRMED,
    APPOINTMENT_COMPLETED,
    APPOINTMENT_NO_SHOW,
)
from .models import Doctor
from .services import get_doctor_week_schedule


def doctor_list_view(request):
    doctors = Doctor.objects.select_related('user').prefetch_related('services').all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})


def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('user').prefetch_related('services', 'schedules'), pk=pk)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})


def doctor_schedule_board_view(request):
    doctors = (
        Doctor.objects
        .select_related('user')
        .prefetch_related('schedules', 'services')
        .order_by('full_name')
    )

    schedule_rows = []

    for doctor in doctors:
        active_keys = {
            (schedule.weekday, schedule.shift)
            for schedule in doctor.schedules.all()
            if schedule.is_active
        }

        cells = []
        for weekday_value, weekday_label in WEEKDAY_CHOICES:
            for shift_value, shift_label in SHIFT_CHOICES:
                cells.append({
                    'weekday': weekday_value,
                    'weekday_label': weekday_label,
                    'shift': shift_value,
                    'shift_label': shift_label,
                    'active': (weekday_value, shift_value) in active_keys,
                })

        schedule_rows.append({
            'doctor': doctor,
            'service_text': doctor.services_display,
            'cells': cells,
        })

    return render(request, 'doctors/schedule_board.html', {
        'schedule_rows': schedule_rows,
        'weekdays': WEEKDAY_CHOICES,
        'shifts': SHIFT_CHOICES,
    })

@login_required
def doctor_portal_view(request):
    if request.user.role != ROLE_DOCTOR or not hasattr(request.user, 'doctor_profile'):
        return render(request, 'doctors/doctor_portal.html', {'error': 'Bạn không có quyền xem trang này.'})

    doctor = request.user.doctor_profile

    appointments = (
    doctor.appointments
    .select_related('customer', 'service')
    .filter(status__in=[
        APPOINTMENT_CONFIRMED,
        APPOINTMENT_COMPLETED,
        APPOINTMENT_NO_SHOW,
    ])
    .order_by('appointment_date', 'shift')
)

    days, schedule_map = get_doctor_week_schedule(doctor)

    return render(request, 'doctors/doctor_portal.html', {
        'doctor': doctor,
        'appointments': appointments,
        'days': days,
        'schedule_map': schedule_map,
    })


@login_required
def doctor_my_appointments_view(request):
    return doctor_portal_view(request)
