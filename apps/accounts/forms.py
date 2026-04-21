from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomerProfile, User
from common.choices import ROLE_CUSTOMER, ROLE_DOCTOR
from common.validators import validate_vietnam_phone


class StyledModelFormMixin:
    def apply_bootstrap(self):
        for name, field in self.fields.items():
            attrs = field.widget.attrs
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            attrs['class'] = css
            attrs['data-label'] = field.label
            if field.required:
                attrs['required'] = 'required'
            if name in ['username', 'email', 'phone', 'password1', 'password2', 'password']:
                attrs.setdefault('autocomplete', 'off')


class RegisterForm(StyledModelFormMixin, UserCreationForm):
    full_name = forms.CharField(max_length=120, label='Họ và tên')
    gender = forms.ChoiceField(choices=CustomerProfile.GENDER_CHOICES, label='Giới tính')
    phone = forms.CharField(max_length=15, label='Số điện thoại', validators=[validate_vietnam_phone])
    email = forms.EmailField(label='Email')

    password1 = forms.CharField(
        label='Mật khẩu',
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )
    password2 = forms.CharField(
        label='Xác nhận mật khẩu',
        widget=forms.PasswordInput,
        strip=False,
        help_text='',
    )

    class Meta:
        model = User
        fields = ['username', 'full_name', 'gender', 'phone', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
        self.fields['username'].widget.attrs.update({'minlength': '4', 'maxlength': '150'})
        self.fields['full_name'].widget.attrs.update({'maxlength': '120'})
        self.fields['phone'].widget.attrs.update({'pattern': r'^(0|\+84)\d{9,10}$', 'inputmode': 'numeric'})
        self.fields['email'].widget.attrs.update({'type': 'email'})
        self.fields['password1'].widget.attrs.update({'minlength': '8'})
        self.fields['password2'].widget.attrs.update({'minlength': '8'})
        for field in self.fields.values():
            field.help_text = ''

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        if len(username) < 4:
            raise ValidationError('Tên đăng nhập phải có ít nhất 4 ký tự.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Tên đăng nhập này đã tồn tại.')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email này đã được sử dụng.')
        return email

    def clean_phone(self):
        phone = (self.cleaned_data.get('phone') or '').strip()
        validate_vietnam_phone(phone)
        return phone

    def clean_password1(self):
        password = self.cleaned_data.get('password1') or ''
        errors = []
        if len(password) < 8:
            errors.append('Mật khẩu phải có ít nhất 8 ký tự.')
        if password.isdigit():
            errors.append('Mật khẩu không được chỉ gồm chữ số.')
        common_passwords = {'12345678', 'password', 'qwerty123', '123456789', '11111111'}
        if password.lower() in common_passwords:
            errors.append('Mật khẩu quá phổ biến, vui lòng chọn mật khẩu khác.')
        if errors:
            raise ValidationError(errors)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Mật khẩu xác nhận không khớp.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = ROLE_CUSTOMER
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                gender=self.cleaned_data['gender'],
            )
        return user


class LoginForm(StyledModelFormMixin, AuthenticationForm):
    username = forms.CharField(label='Tên đăng nhập')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': 'Tên đăng nhập hoặc mật khẩu không đúng.',
        'inactive': 'Tài khoản hiện đang bị khóa.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.is_staff or user.is_superuser:
            raise ValidationError('Tài khoản quản trị vui lòng đăng nhập tại trang /admin/.', code='admin_login_only')


class DoctorLoginForm(StyledModelFormMixin, AuthenticationForm):
    username = forms.CharField(label='Tài khoản bác sĩ')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': 'Thông tin đăng nhập bác sĩ không chính xác.',
        'inactive': 'Tài khoản bác sĩ hiện đang bị khóa.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if user.role != ROLE_DOCTOR:
            raise ValidationError('Tài khoản này không thuộc bác sĩ.', code='doctor_only')


class ProfileForm(StyledModelFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'gender', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
