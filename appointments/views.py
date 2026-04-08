from django.shortcuts import render, redirect
from django.contrib import messages
<<<<<<< HEAD
from .models import Appointment, Doctor
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
=======
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
from .forms import UserRegistrationForm
from django.contrib.auth import logout

def home_view(request):
    if request.method == "POST":
        # 1. Lấy dữ liệu từ Form
        gender = request.POST.get('gender')
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        branch = request.POST.get('branch')
        appointment_date = request.POST.get('appointment_date')
        note = request.POST.get('note')
        
        # 2. Kiểm tra bắt buộc
        if fullname and phone:
            if not appointment_date:
                appointment_date = None

            # 3. Lưu vào Database
            Appointment.objects.create(
<<<<<<< HEAD
                user=request.user if request.user.is_authenticated else None,
=======
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
                gender=gender,
                fullname=fullname,
                phone=phone,
                service=service,
                branch=branch,
                appointment_date=appointment_date,
                note=note
            )
            
            # 4. GỬI EMAIL THÔNG BÁO (Gộp vào đây)
            try:
                subject = f"CÓ KHÁCH HÀNG MỚI: {fullname}"
                message = f"""
                Chào bạn, hệ thống Nha Khoa 5 Anh Em vừa nhận được lịch hẹn mới:
                - Họ tên: {fullname}
                - Số điện thoại: {phone}
                - Dịch vụ: {service}
                - Chi nhánh: {branch}
                - Ngày hẹn: {appointment_date}
                - Ghi chú: {note}
                
                Hãy gọi lại tư vấn ngay cho khách nhé!
                """
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    ['lam_2251220242@dau.edu.vn'], # Email nhận thông báo
                    fail_silently=False,
                )
                print("--- GỬI MAIL THÀNH CÔNG ---")
            except Exception as e:
                print(f"--- LỖI GỬI MAIL: {e} ---")

            messages.success(request, "Success")
<<<<<<< HEAD
=======
            return redirect('home')
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
            return redirect('appointments:home_view')
        else:
            messages.error(request, "Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")

    return render(request, 'index.html')

# --- CÁC HÀM HIỂN THỊ TRANG KHÁC (GIỮ NGUYÊN) ---
def doctors_page_view(request):
<<<<<<< HEAD
    doctors = Doctor.objects.prefetch_related('schedules').all()
    return render(request, 'doctors.html', {'doctors': doctors})
=======
    return render(request, 'doctors.html')
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be

def price_list_view(request):
    return render(request, 'price_list.html')

<<<<<<< HEAD
@login_required
def appointment_history_view(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'appointment_history.html', {'appointments': appointments})

=======
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công. Vui lòng đăng nhập.')
<<<<<<< HEAD
            return redirect('appointments:auth')
=======
            return redirect('appointments:login')
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

<<<<<<< HEAD
def auth_view(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'first_name' not in request.POST:
            # Login form submitted
            from django.contrib.auth import authenticate, login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Chào mừng {user.get_full_name() or user.username}!')
                return redirect('appointments:home_view')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
                return redirect('appointments:auth')
        else:
            # Register form submitted
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Đăng ký thành công. Vui lòng đăng nhập.')
                return redirect('appointments:auth')
            else:
                # If register form has errors, show them
                return render(request, 'auth.html', {
                    'register_form': form,
                    'login_form_errors': True
                })
    
    # GET request - show both forms
    return render(request, 'auth.html', {
        'register_form': UserRegistrationForm(),
        'login_form_errors': False
    })

def logout_view(request):
    logout(request)
    return redirect('/')

def about_view(request):
    return render(request, 'about.html')

def services_view(request):
    return render(request, 'services.html')

def contact_view(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject', 'Contact Form')
        message_text = request.POST.get('message')
        
        if fullname and email and message_text:
            try:
                admin_message = f"New contact from {fullname}:\nEmail: {email}\nPhone: {phone}\nSubject: {subject}\n\nMessage:\n{message_text}"
                send_mail(f"Contact: {subject}", admin_message, settings.EMAIL_HOST_USER, ['lam_2251220242@dau.edu.vn'], fail_silently=False)
                messages.success(request, 'Tin nhan da gui thanh cong!')
            except Exception as e:
                messages.error(request, 'Loi gui tin nhan')
        else:
            messages.error(request, 'Vui long dien day du thong tin')
        return redirect('appointments:contact')
    return render(request, 'contact.html')
=======
def logout_view(request):
    logout(request)
    return redirect('/')
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
# ...existing code...