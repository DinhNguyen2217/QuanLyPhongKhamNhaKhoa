# ...existing code...
from django.db import models, transaction
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import date

PHONE_VALIDATOR = RegexValidator(r'^\d{9,12}$', 'Số điện thoại chỉ chứa chữ số (9-12 chữ số).')

ROLE_CHOICES = (
    ('customer','Customer'),
    ('doctor','Doctor'),
    ('admin','Admin'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Doctor(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=80, blank=True)
    specialty = models.CharField(max_length=120, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name
=======
    name = models.CharField(max_length=150, verbose_name="Họ tên")
    title = models.CharField(max_length=80, blank=True, verbose_name="Chức vụ") # Ví dụ: Trưởng khoa, Bác sĩ chính
    qualification = models.CharField(max_length=120, blank=True, verbose_name="Trình độ") # Ví dụ: Tiến sĩ, Thạc sĩ, Cử nhân
    specialty = models.CharField(max_length=120, blank=True, verbose_name="Chuyên khoa")
    experience_years = models.PositiveSmallIntegerField(default=0, verbose_name="Số năm kinh nghiệm")
    bio = models.TextField(blank=True, verbose_name="Tiểu sử")
    avatar = models.CharField(max_length=255, blank=True, verbose_name="Link ảnh đại diện")
    
    def __str__(self):
        return f"{self.title}. {self.name}"
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)

class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Schedule(models.Model):
    SHIFT_CHOICES = (('morning','Ca sáng'), ('afternoon','Ca chiều'))
<<<<<<< HEAD
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=[(i,str(i)) for i in range(0,7)])  # 0=Mon..6=Sun
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    def __str__(self):
        return f"{self.doctor.name} - {self.get_shift_display()} - {self.weekday}"
=======
    WEEKDAY_CHOICES = [
        (0, 'Thứ Hai'), (1, 'Thứ Ba'), (2, 'Thứ Tư'), 
        (3, 'Thứ Năm'), (4, 'Thứ Sáu'), (5, 'Thứ Bảy'), (6, 'Chủ Nhật'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, verbose_name="Ngày trực")
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES, verbose_name="Ca trực")

    class Meta:
        # Đảm bảo một bác sĩ không bị trùng lịch trực trong cùng 1 buổi
        unique_together = ('doctor', 'weekday', 'shift')
        verbose_name = "Lịch làm việc"
        verbose_name_plural = "Lịch làm việc"

    def __str__(self):
        return f"{self.doctor.name} - {self.get_weekday_display()} - {self.get_shift_display()}"
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)

class Appointment(models.Model):
    SHIFT_CHOICES = (('morning','Ca sáng'), ('afternoon','Ca chiều'))
    STATUS_CHOICES = (('pending','Pending'), ('confirmed','Confirmed'), ('cancelled','Cancelled'))

    fullname = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR])
    gender = models.CharField(max_length=10, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=date.today)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    symptom = models.TextField(blank=True)
    deposit = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['date','shift']),]
        ordering = ['-date','shift']

    @classmethod
    def booked_count(cls, date, shift):
        return cls.objects.filter(date=date, shift=shift, status__in=['pending','confirmed']).count()

    @classmethod
    def available_slots(cls, date, shift, max_per_shift=10):
        return max(0, max_per_shift - cls.booked_count(date, shift))

    @classmethod
    def create_with_slot_check(cls, *, fullname, phone, date, shift, service=None, doctor=None, symptom='', deposit=0, max_per_shift=10):
        with transaction.atomic():
            if cls.available_slots(date, shift, max_per_shift) <= 0:
                raise ValueError('Đã đủ số lượng đặt cho ca này.')
            return cls.objects.create(
                fullname=fullname, phone=phone, date=date, shift=shift,
                service=service, doctor=doctor, symptom=symptom, deposit=deposit
<<<<<<< HEAD
            )
    
=======
            )
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
