from django.contrib import admin
from .models import Appointment # Hoặc tên Model bạn đã đặt

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'created_at') # Hiện các cột này ra danh sách
    search_fields = ('fullname', 'phone') # Cho phép tìm kiếm theo tên hoặc số ĐT