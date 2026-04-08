# ...existing code...
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'appointments'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('register/', views.register, name='register'),
    path('login/', views.auth_view, name='login'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('gioi-thieu/', views.about_view, name='about'),
    path('dich-vu/', views.services_view, name='services'),
    path('lien-he/', views.contact_view, name='contact'),
    path('doi-ngu-bac-si/', views.doctors_page_view, name='doctors_page'),
    path('bang-gia/', views.price_list_view, name='price_page'),
    path('lich-su-dat-lich/', views.appointment_history_view, name='history'),
]
# ...existing code...