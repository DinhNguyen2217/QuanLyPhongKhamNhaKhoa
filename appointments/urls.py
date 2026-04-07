# ...existing code...
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'appointments'

urlpatterns = [
<<<<<<< HEAD
=======
    # Các link cũ của bạn (Giữ nguyên)
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
    path('', views.home_view, name='home_view'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
<<<<<<< HEAD
    path('doi-ngu-bac-si/', views.doctors_page_view, name='doctors_page'),
    path('bang-gia/', views.price_list_view, name='price_page'),
=======
    path('bang-gia/', views.price_list_view, name='price_page'),
    
    # --- PHẦN CẬP NHẬT VỀ ĐỐI TƯỢNG BÁC SĨ ---
    
    # Trang danh sách đội ngũ bác sĩ
    path('doi-ngu-bac-si/', views.doctors_page_view, name='doctors_page'),
    
    # Trang chi tiết thông tin của từng bác sĩ (truyền ID bác sĩ)
    path('doi-ngu-bac-si/<int:pk>/', views.doctor_detail_view, name='doctor_detail'),
    
    # Trang lịch làm việc chung (Bảng lịch trực tuần)
    path('lich-lam-viec/', views.general_schedule_view, name='schedule_page'),
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
]
# ...existing code...