# ...existing code...
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, PHONE_VALIDATOR
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label='Xác nhận mật khẩu', widget=forms.PasswordInput, min_length=8)
    phone = forms.CharField(label='Số điện thoại', validators=[PHONE_VALIDATOR], required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Gán class + placeholder cho widget để template có thể render trực tiếp {{ form.field }}
        attrs = {
            'first_name': {'class': 'form-control', 'placeholder': 'Họ'},
            'last_name': {'class': 'form-control', 'placeholder': 'Tên'},
            'username': {'class': 'form-control', 'placeholder': 'Tên đăng nhập'},
            'email': {'class': 'form-control', 'placeholder': 'Email'},
            'phone': {'class': 'form-control', 'placeholder': '0912xxxxxx'},
            'password1': {'class': 'form-control', 'placeholder': 'Mật khẩu (ít nhất 8 ký tự)'},
            'password2': {'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'},
        }
        for name, a in attrs.items():
            if name in self.fields:
                self.fields[name].widget.attrs.update(a)

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if not p1 or not p2:
            raise ValidationError("Vui lòng nhập mật khẩu và xác nhận mật khẩu.")
        if p1 != p2:
            raise ValidationError("Mật khẩu và xác nhận mật khẩu không khớp.")
        return p2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Tên đăng nhập đã tồn tại.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email này đã được sử dụng.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # tạo/hoặc cập nhật profile với số điện thoại
            try:
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.phone = self.cleaned_data.get('phone')
                profile.save()
            except Exception:
                pass
        return user
# ...existing code...