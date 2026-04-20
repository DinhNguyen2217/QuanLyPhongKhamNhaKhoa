from django.urls import path
from . import placeholder_views as views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.appointments_book, name='book'),
    path('availability/', views.appointments_availability, name='availability'),
    path('created/<int:pk>/', views.appointments_created, name='booking_created'),
    path('history/', views.appointments_history, name='history'),
    path('confirm/<uuid:token>/', views.appointments_confirm_email, name='confirm_email'),
    path('payment/<int:pk>/', views.appointments_payment, name='payment'),
    path('payment/<int:pk>/status/', views.appointments_payment_status, name='payment_status'),
    path('fake-pay/<uuid:token>/', views.appointments_fake_gateway, name='fake_gateway'),
    path('fake-pay/<uuid:token>/confirm/', views.appointments_fake_gateway_confirm, name='fake_gateway_confirm'),
]
