from django.urls import path
from .views import doctor_detail_view, doctor_list_view, doctor_my_appointments_view, doctor_portal_view, doctor_schedule_board_view

app_name = 'doctors'

urlpatterns = [
    path('', doctor_list_view, name='doctor_list'),
    path('schedule/', doctor_schedule_board_view, name='schedule_board'),
    path('portal/', doctor_portal_view, name='portal'),
    path('my-appointments/', doctor_my_appointments_view, name='my_appointments'),
    path('<int:pk>/', doctor_detail_view, name='doctor_detail'),
]
