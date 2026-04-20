import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from common.choices import (
    APPOINTMENT_PENDING_EMAIL,
    APPOINTMENT_STATUS_CHOICES,
    PAYMENT_STATUS_CHOICES,
    PAYMENT_UNPAID,
    SHIFT_CHOICES,
)
from common.validators import validate_vietnam_phone


class Appointment(models.Model):
    GENDER_CHOICES = [('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Khách hàng', on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey('doctors.Doctor', verbose_name='Bác sĩ', on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    service = models.ForeignKey('catalog.Service', verbose_name='Dịch vụ', on_delete=models.CASCADE, related_name='appointments')
    full_name = models.CharField('Họ và tên', max_length=120)
    email = models.EmailField('Email')
    phone = models.CharField('Số điện thoại', max_length=15, validators=[validate_vietnam_phone])
    gender = models.CharField('Giới tính', max_length=10, choices=GENDER_CHOICES, default='other')
    symptom = models.TextField('Triệu chứng', blank=True)
    appointment_date = models.DateField('Ngày khám')
    shift = models.CharField('Buổi khám', max_length=20, choices=SHIFT_CHOICES)
    status = models.CharField('Trạng thái lịch hẹn', max_length=30, choices=APPOINTMENT_STATUS_CHOICES, default=APPOINTMENT_PENDING_EMAIL)
    payment_status = models.CharField('Trạng thái thanh toán', max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_UNPAID)
    deposit_amount = models.DecimalField('Tiền cọc', max_digits=12, decimal_places=0, default=100000)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField('Thời gian tạo', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lịch hẹn'
        verbose_name_plural = 'Lịch hẹn'

    def __str__(self):
        return f"{self.full_name} - {self.service.name} - {self.appointment_date}"

    def get_confirm_path(self):
        return reverse('appointments:confirm_email', args=[str(self.email_token)])


class PaymentTransaction(models.Model):
    appointment = models.OneToOneField(Appointment, verbose_name='Lịch hẹn', on_delete=models.CASCADE, related_name='payment')
    transaction_code = models.UUIDField('Mã giao dịch', default=uuid.uuid4, editable=False, unique=True)
    amount = models.DecimalField('Số tiền', max_digits=12, decimal_places=0)
    status = models.CharField('Trạng thái', max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_UNPAID)
    method = models.CharField('Phương thức', max_length=50, default='fake_gateway')
    paid_at = models.DateTimeField('Thanh toán lúc', null=True, blank=True)
    created_at = models.DateTimeField('Thời gian tạo', auto_now_add=True)

    class Meta:
        verbose_name = 'Giao dịch thanh toán'
        verbose_name_plural = 'Giao dịch thanh toán'

    def __str__(self):
        return str(self.transaction_code)
