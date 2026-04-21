# Phân chia module cho 5 thành viên

## Thành viên 1 - Base + Accounts
Phụ trách các thư mục:
- `config/`
- `common/`
- `apps/accounts/`
- `requirements.txt`
- `README.md`

Nhiệm vụ:
- cấu hình Django, MySQL/SQLite
- custom user, phân quyền
- đăng ký, đăng nhập, đăng xuất
- validation chung
- luồng email cơ bản

## Thành viên 2 - Dashboard Admin
Phụ trách:
- `apps/dashboard/`

Nhiệm vụ:
- dashboard thống kê
- danh sách lịch hẹn tổng quát
- mở rộng CRUD admin nếu cần

## Thành viên 3 - Doctors
Phụ trách:
- `apps/doctors/`

Nhiệm vụ:
- model bác sĩ
- lịch làm việc bác sĩ
- danh sách bác sĩ
- chi tiết bác sĩ
- trang bác sĩ xem lịch hẹn của mình

## Thành viên 4 - Appointments
Phụ trách:
- `apps/appointments/`

Nhiệm vụ:
- đặt lịch
- auto gán bác sĩ
- kiểm tra slot
- email xác nhận
- fake payment
- lịch sử đặt lịch

## Thành viên 5 - UI + Catalog + Core
Phụ trách:
- `apps/catalog/`
- `apps/core/`
- `templates/`
- `static/`

Nhiệm vụ:
- giao diện tổng thể
- trang chủ, giới thiệu, liên hệ
- dịch vụ, gói sản phẩm, bảng giá
- chỉnh CSS, responsive, base template

## Nguyên tắc làm GitHub
- mỗi người tạo 1 nhánh riêng từ `develop`
- commit đúng module mình phụ trách
- không sửa lung tung file của người khác
- file chung như `config/settings.py`, `config/urls.py`, `templates/base.html` nên thống nhất qua trưởng nhóm trước khi sửa
