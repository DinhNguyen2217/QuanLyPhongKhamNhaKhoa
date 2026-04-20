from django.urls import path
from .views import CustomLoginView, CustomLogoutView, DoctorLoginView, profile_view, register_view

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('doctor-login/', DoctorLoginView.as_view(), name='doctor_login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
]
