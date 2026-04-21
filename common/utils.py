from datetime import timedelta
from django.utils import timezone


def start_of_week(date=None):
    if date is None:
        date = timezone.localdate()
    return date - timedelta(days=date.weekday())
