# Clinic Booking - Website quản lý đặt lịch nha khoa

Dự án Django được chia theo 5 module để nhóm dễ phân công và commit GitHub.

## Thành viên gợi ý theo module
- Người 1: `config/`, `common/`, `apps/accounts/`
- Người 2: `apps/dashboard/`
- Người 3: `apps/doctors/`
- Người 4: `apps/appointments/`
- Người 5: `apps/catalog/`, `apps/core/`, `templates/`, `static/`

## Chức năng hiện có
- Trang chủ, giới thiệu, liên hệ
- Danh sách dịch vụ, gói sản phẩm, bảng giá
- Danh sách bác sĩ, lịch làm việc, chi tiết bác sĩ
- Đăng ký, đăng nhập, đăng xuất, hồ sơ người dùng
- Đặt lịch tự gán bác sĩ theo chuyên môn và ca trực
- Xác nhận lịch qua email token
- Fake thanh toán cọc
- Lịch sử đặt lịch của khách hàng
- Dashboard admin cơ bản
- Lịch làm việc và lịch hẹn của bác sĩ

## 1. Tạo môi trường
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Tạo file môi trường
Copy `.env.example` thành `.env` rồi chỉnh nếu muốn dùng MySQL.

## 3. Chạy bằng SQLite mặc định
Nếu chưa cấu hình MySQL, hệ thống sẽ tự dùng SQLite để demo.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 4. Dùng MySQL Workbench / MySQL Server
Trong `.env`, đổi:
```env
USE_MYSQL=True
MYSQL_DB=clinic_booking
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```
Sau đó tạo database `clinic_booking` trong MySQL Workbench và chạy migrate lại.

## 5. Email xác nhận
Mặc định dùng backend console, nên khi đặt lịch, link xác nhận sẽ in ra terminal.
Nếu muốn demo đẹp hơn có thể đổi sang file backend trong `config/settings.py`.

## 6. Quy trình làm nhóm trên GitHub
- `main`: bản ổn định
- `develop`: bản tích hợp
- mỗi người tạo 1 nhánh riêng rồi merge vào `develop`

Ví dụ:
```bash
git checkout -b feature/accounts-nguyen
git checkout -b feature/dashboard-khanh
git checkout -b feature/doctors-sang
git checkout -b feature/appointments-thao
git checkout -b feature/ui-lam
```
