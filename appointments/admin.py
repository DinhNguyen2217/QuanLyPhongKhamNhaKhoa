from django.contrib import admin
<<<<<<< HEAD
from .models import Appointment # Hoặc tên Model bạn đã đặt

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'created_at') # Hiện các cột này ra danh sách
    search_fields = ('fullname', 'phone') # Cho phép tìm kiếm theo tên hoặc số ĐT
=======
from .models import Appointment, UserProfile, Doctor, Schedule, Service # Import thêm các model mới

# Giữ nguyên code Appointment cũ của bạn
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'date', 'shift', 'status', 'created_at') # Thêm cột date, shift, status cho dễ nhìn
    search_fields = ('fullname', 'phone')
    list_filter = ('date', 'status', 'shift') # Thêm bộ lọc bên phải

# --- BỔ SUNG CÁC MODEL MỚI THEO YÊU CẦU ---

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Hiển thị các thông tin cơ bản của bác sĩ trong danh sách
    list_display = ('name', 'title', 'qualification', 'specialty', 'experience_years')
    search_fields = ('name', 'specialty')
    list_filter = ('title', 'qualification')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    # Hiển thị lịch trực: Bác sĩ nào, trực thứ mấy, ca nào
    list_display = ('doctor', 'get_weekday_display', 'get_shift_display')
    list_filter = ('weekday', 'shift', 'doctor')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
