from django.contrib import admin
from .models import Appointment, PaymentTransaction


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service', 'doctor', 'appointment_date', 'shift', 'status', 'payment_status')
    list_filter = ('status', 'payment_status', 'shift', 'appointment_date')
    search_fields = ('full_name', 'email', 'phone', 'service__name', 'doctor__full_name', 'doctor__user__username')


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_code', 'appointment', 'amount', 'status', 'method', 'paid_at')
    list_filter = ('status', 'method')
