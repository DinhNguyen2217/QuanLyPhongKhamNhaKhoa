from django.urls import path
from .views import (
    book_appointment_view,
    booking_created_view,
    confirm_email_view,
    doctor_availability_view,
    fake_gateway_confirm_view,
    fake_gateway_view,
    history_view,
    payment_status_view,
    payment_view,
)

app_name = 'appointments'

urlpatterns = [
    path('book/', book_appointment_view, name='book'),
    path('availability/', doctor_availability_view, name='availability'),
    path('created/<int:pk>/', booking_created_view, name='booking_created'),
    path('history/', history_view, name='history'),
    path('confirm/<uuid:token>/', confirm_email_view, name='confirm_email'),
    path('payment/<int:pk>/', payment_view, name='payment'),
    path('payment/<int:pk>/status/', payment_status_view, name='payment_status'),
    path('fake-pay/<uuid:token>/', fake_gateway_view, name='fake_gateway'),
    path('fake-pay/<uuid:token>/confirm/', fake_gateway_confirm_view, name='fake_gateway_confirm'),
]
