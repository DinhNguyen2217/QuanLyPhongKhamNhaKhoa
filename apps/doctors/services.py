from datetime import timedelta
from common.utils import start_of_week
from .models import Doctor


def get_week_schedule_matrix():
    start = start_of_week()
    days = [start + timedelta(days=i) for i in range(7)]
    doctors = Doctor.objects.select_related('user').prefetch_related('schedules', 'services').all()
    return doctors, days


def get_doctor_week_schedule(doctor):
    start = start_of_week()
    days = [start + timedelta(days=i) for i in range(7)]
    schedule_map = {day.weekday(): [] for day in days}
    for item in doctor.schedules.filter(is_active=True).order_by('weekday', 'shift'):
        schedule_map[item.weekday].append(item)
    return days, schedule_map
