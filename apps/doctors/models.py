from django.conf import settings
from django.db import models
from common.choices import SHIFT_CHOICES, WEEKDAY_CHOICES


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Tài khoản', on_delete=models.CASCADE, related_name='doctor_profile')
    full_name = models.CharField('Họ và tên', max_length=120)
    age = models.PositiveIntegerField('Tuổi', default=30)
    years_of_experience = models.PositiveIntegerField('Số năm kinh nghiệm', default=1)
    qualification = models.CharField('Trình độ', max_length=255)
    achievement = models.TextField('Thành tựu', blank=True)
    position = models.CharField('Chức vụ', max_length=120)
    bio = models.TextField('Giới thiệu', blank=True)
    avatar = models.ImageField('Ảnh đại diện', upload_to='doctors/', blank=True, null=True)
    services = models.ManyToManyField('catalog.Service', verbose_name='Dịch vụ phụ trách', related_name='doctors', blank=True)

    class Meta:
        verbose_name = 'Bác sĩ'
        verbose_name_plural = 'Bác sĩ'

    @property
    def display_name(self):
        return self.full_name or self.user.get_full_name() or self.user.username

    @property
    def services_display(self):
        return ', '.join(self.services.values_list('name', flat=True)) or 'Chưa gán dịch vụ'

    def __str__(self):
        return self.display_name


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name='Bác sĩ', on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField('Thứ', choices=WEEKDAY_CHOICES)
    shift = models.CharField('Ca làm việc', max_length=20, choices=SHIFT_CHOICES)
    is_active = models.BooleanField('Đang hoạt động', default=True)

    class Meta:
        unique_together = ('doctor', 'weekday', 'shift')
        ordering = ['weekday', 'shift']
        verbose_name = 'Lịch làm việc bác sĩ'
        verbose_name_plural = 'Lịch làm việc bác sĩ'

    def __str__(self):
        return f"{self.doctor} - {self.get_weekday_display()} - {self.get_shift_display()}"
