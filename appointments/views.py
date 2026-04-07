<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Appointment
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment, Doctor, Schedule # Import thêm Doctor và Schedule
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegistrationForm
from django.contrib.auth import logout

def home_view(request):
    if request.method == "POST":
<<<<<<< HEAD
        # 1. Lấy dữ liệu từ Form
=======
        # ... (Giữ nguyên logic POST và gửi mail cũ của bạn) ...
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
        gender = request.POST.get('gender')
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        service = request.POST.get('service')
        branch = request.POST.get('branch')
        appointment_date = request.POST.get('appointment_date')
        note = request.POST.get('note')
        
<<<<<<< HEAD
        # 2. Kiểm tra bắt buộc
        if fullname and phone:
            if not appointment_date:
                appointment_date = None

            # 3. Lưu vào Database
            Appointment.objects.create(
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
            return redirect('home')
            return redirect('appointments:home_view')
=======
        if fullname and phone:
            if not appointment_date: appointment_date = None

            Appointment.objects.create(
                gender=gender, fullname=fullname, phone=phone,
                service=service, branch=branch, 
                date=appointment_date, # Lưu ý: Model của bạn trường này là 'date'
                symptom=note # Lưu ý: Model của bạn dùng 'symptom' thay vì 'note'
            )
            
            try:
                subject = f"CÓ KHÁCH HÀNG MỚI: {fullname}"
                message = f"Thông tin đặt lịch:\n- Tên: {fullname}\n- SĐT: {phone}\n..."
                send_mail(subject, message, settings.EMAIL_HOST_USER, ['lam_2251220242@dau.edu.vn'], fail_silently=False)
            except Exception as e:
                print(f"Lỗi gửi mail: {e}")

            messages.success(request, "Đặt lịch thành công!")
            return redirect('home')
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
        else:
            messages.error(request, "Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")

    return render(request, 'index.html')

<<<<<<< HEAD
# --- CÁC HÀM HIỂN THỊ TRANG KHÁC (GIỮ NGUYÊN) ---
def doctors_page_view(request):
    return render(request, 'doctors.html')

=======
# --- PHẦN CHỈNH SỬA & BỔ SUNG MỚI ---

# 1. Trang danh sách bác sĩ (Cập nhật)
def doctors_page_view(request):
    doctors = Doctor.objects.all() # Lấy toàn bộ danh sách bác sĩ
    return render(request, 'doctors.html', {'doctors': doctors})

# 2. Trang chi tiết từng bác sĩ (Bổ sung mới)
def doctor_detail_view(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # Lấy lịch trực của riêng bác sĩ này
    schedules = doctor.schedules.all().order_by('weekday')
    return render(request, 'doctor_detail.html', {
        'doctor': doctor,
        'schedules': schedules
    })

# 3. Trang Lịch làm việc chung (Bổ sung mới)
def general_schedule_view(request):
    # Tạo cấu trúc dữ liệu cho bảng lịch tuần
    days = [0, 1, 2, 3, 4, 5, 6] # Thứ 2 đến Chủ nhật
    schedule_data = []
    
    for day_code in days:
        day_name = dict(Schedule.WEEKDAY_CHOICES).get(day_code)
        # Lấy các bác sĩ trực ca sáng và chiều của ngày này
        morning_shifts = Schedule.objects.filter(weekday=day_code, shift='morning').select_related('doctor')
        afternoon_shifts = Schedule.objects.filter(weekday=day_code, shift='afternoon').select_related('doctor')
        
        schedule_data.append({
            'day_name': day_name,
            'morning': morning_shifts,
            'afternoon': afternoon_shifts
        })

    return render(request, 'general_schedule.html', {'schedule_grid': schedule_data})

# --- CÁC HÀM CÒN LẠI GIỮ NGUYÊN ---
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
def price_list_view(request):
    return render(request, 'price_list.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công. Vui lòng đăng nhập.')
            return redirect('appointments:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
<<<<<<< HEAD
    return redirect('/')
# ...existing code...
=======
    return redirect('/')
>>>>>>> c7fbb98 (DuySang01: Hoàn thiện chức năng Bác sĩ và Lịch làm việc)
