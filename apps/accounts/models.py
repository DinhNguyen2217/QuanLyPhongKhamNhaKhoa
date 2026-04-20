from django.contrib.auth.models import AbstractUser
from django.db import models
from common.choices import ROLE_CHOICES, ROLE_CUSTOMER
from common.validators import validate_vietnam_phone


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    role = models.CharField('Vai trò', max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)
    phone = models.CharField('Số điện thoại', max_length=15, validators=[validate_vietnam_phone], blank=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Tài khoản'
        verbose_name_plural = 'Tài khoản'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"


class CustomerProfile(models.Model):
    GENDER_CHOICES = [('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')]

    user = models.OneToOneField(User, verbose_name='Tài khoản', on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField('Họ và tên', max_length=120)
    gender = models.CharField('Giới tính', max_length=10, choices=GENDER_CHOICES, default='other')
    address = models.CharField('Địa chỉ', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Hồ sơ khách hàng'
        verbose_name_plural = 'Hồ sơ khách hàng'

    def __str__(self):
        return self.full_name
