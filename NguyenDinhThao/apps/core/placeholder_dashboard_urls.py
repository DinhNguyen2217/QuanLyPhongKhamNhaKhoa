from django.urls import path
from . import placeholder_views as views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('doctor-schedule/', views.dashboard_doctor_schedule, name='doctor_schedule_manage'),
]
