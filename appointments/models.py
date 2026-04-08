<<<<<<< HEAD
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
=======
# ...existing code...
from django.db import models, transaction
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import date
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be

PHONE_VALIDATOR = RegexValidator(r'^\d{9,12}$', 'Số điện thoại chỉ chứa chữ số (9-12 chữ số).')

ROLE_CHOICES = (
<<<<<<< HEAD
    ('customer', 'Customer'),
    ('doctor', 'Doctor'),
    ('admin', 'Admin'),
=======
    ('customer','Customer'),
    ('doctor','Doctor'),
    ('admin','Admin'),
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, validators=[PHONE_VALIDATOR], blank=True, null=True)
<<<<<<< HEAD

=======
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Doctor(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=200)
    specialty = models.CharField(max_length=200, verbose_name='Chuyên khoa')
    experience = models.TextField(verbose_name='Mô tả ngắn')
    details = models.TextField(blank=True, verbose_name='Chi tiết')
    highlights = models.TextField(blank=True, verbose_name='Điểm mạnh', help_text='Nhập mỗi điểm mạnh trên một dòng')
    image_url = models.URLField(max_length=500, verbose_name='Link ảnh bác sĩ', blank=True)

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    def get_highlights(self):
        return [item.strip() for item in self.highlights.splitlines() if item.strip()]

class DoctorSchedule(models.Model):
    DAY_CHOICES = (
        ('Thứ 2', 'Thứ 2'),
        ('Thứ 3', 'Thứ 3'),
        ('Thứ 4', 'Thứ 4'),
        ('Thứ 5', 'Thứ 5'),
        ('Thứ 6', 'Thứ 6'),
        ('Thứ 7', 'Thứ 7'),
        ('Chủ nhật', 'Chủ nhật'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20, choices=DAY_CHOICES, verbose_name='Ngày trong tuần')
    start_time = models.TimeField(verbose_name='Bắt đầu')
    end_time = models.TimeField(verbose_name='Kết thúc')
    notes = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ghi chú')

    class Meta:
        ordering = ['doctor', 'day', 'start_time']
        verbose_name = 'Lịch làm việc'
        verbose_name_plural = 'Lịch làm việc'

    def __str__(self):
        return f"{self.doctor.name} - {self.day} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Tiêu đề')
    content = models.TextField(verbose_name='Nội dung')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày đăng')
    image_url = models.URLField(max_length=500, verbose_name='Link ảnh minh họa')

    def __str__(self):
        return self.title

class ServicePrice(models.Model):
    service_name = models.CharField(max_length=200, verbose_name='Tên dịch vụ')
    unit = models.CharField(max_length=50, verbose_name='Đơn vị')
    price = models.IntegerField(verbose_name='Giá tiền')

    class Meta:
        verbose_name = 'Bảng giá'
        verbose_name_plural = 'Quản lý bảng giá'

    def __str__(self):
        return self.service_name

class Appointment(models.Model):
    GENDER_CHOICES = (('Anh', 'Anh'), ('Chị', 'Chị'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Người dùng')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='Danh xưng')
    fullname = models.CharField(max_length=255, verbose_name='Họ tên')
    phone = models.CharField(max_length=20, validators=[PHONE_VALIDATOR], verbose_name='Số điện thoại')
    service = models.CharField(max_length=100, blank=True, null=True, verbose_name='Dịch vụ quan tâm')
    branch = models.CharField(max_length=255, blank=True, null=True, verbose_name='Chi nhánh')
    appointment_date = models.DateField(blank=True, null=True, verbose_name='Ngày hẹn dự kiến')
    note = models.TextField(blank=True, null=True, verbose_name='Mong muốn khách hàng')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Thời điểm đặt')

    def __str__(self):
        return f"{self.fullname} - {self.service or 'Chưa chọn dịch vụ'}"
=======
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=80, blank=True)
    specialty = models.CharField(max_length=120, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Schedule(models.Model):
    SHIFT_CHOICES = (('morning','Ca sáng'), ('afternoon','Ca chiều'))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=[(i,str(i)) for i in range(0,7)])  # 0=Mon..6=Sun
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    def __str__(self):
        return f"{self.doctor.name} - {self.get_shift_display()} - {self.weekday}"

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
            )
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
    