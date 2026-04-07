# ...existing code...
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'appointments'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doi-ngu-bac-si/', views.doctors_page_view, name='doctors_page'),
    path('bang-gia/', views.price_list_view, name='price_page'),
]
# ...existing code...