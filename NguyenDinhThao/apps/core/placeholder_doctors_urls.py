from django.urls import path
from . import placeholder_views as views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctors_list, name='doctor_list'),
    path('schedule/', views.doctors_schedule, name='schedule_board'),
    path('portal/', views.doctors_portal, name='portal'),
    path('my-appointments/', views.doctors_my_appointments, name='my_appointments'),
    path('<int:pk>/', views.doctors_detail, name='doctor_detail'),
]
