from django.urls import path
from .views import dashboard_home_view, doctor_schedule_manage_view

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_home_view, name='home'),
    path('doctor-schedule/', doctor_schedule_manage_view, name='doctor_schedule_manage'),
]
