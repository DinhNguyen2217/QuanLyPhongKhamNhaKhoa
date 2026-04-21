from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render
from common.choices import ROLE_DOCTOR
from .forms import DoctorLoginForm, LoginForm, ProfileForm, RegisterForm
from .services import ensure_customer_profile


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.role == ROLE_DOCTOR:
            return reverse('doctors:portal')
        return reverse('core:home')


class DoctorLoginView(LoginView):
    form_class = DoctorLoginForm
    template_name = 'accounts/doctor_login.html'

    def get_success_url(self):
        return reverse('doctors:portal')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Đăng ký thành công.')
        return redirect('core:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile = ensure_customer_profile(request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.user.phone = request.POST.get('phone', request.user.phone)
        request.user.save()
        messages.success(request, 'Cập nhật hồ sơ thành công.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})
