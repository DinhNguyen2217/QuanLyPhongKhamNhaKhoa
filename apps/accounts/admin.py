from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Thông tin đăng nhập', {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email', 'phone', 'role')}),
        ('Phân quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Mốc thời gian', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('Tạo tài khoản mới', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('username', 'email', 'phone', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'gender', 'address')
    search_fields = ('full_name', 'user__username', 'user__email', 'address')
    list_filter = ('gender',)
