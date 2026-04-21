ROLE_CUSTOMER = 'customer'
ROLE_DOCTOR = 'doctor'
ROLE_ADMIN = 'admin'

ROLE_CHOICES = [
    (ROLE_CUSTOMER, 'Khách hàng'),
    (ROLE_DOCTOR, 'Bác sĩ'),
    (ROLE_ADMIN, 'Quản trị viên'),
]

SHIFT_MORNING = 'morning'
SHIFT_AFTERNOON = 'afternoon'
SHIFT_CHOICES = [
    (SHIFT_MORNING, 'Ca sáng'),
    (SHIFT_AFTERNOON, 'Ca chiều'),
]

WEEKDAY_CHOICES = [
    (0, 'Thứ 2'),
    (1, 'Thứ 3'),
    (2, 'Thứ 4'),
    (3, 'Thứ 5'),
    (4, 'Thứ 6'),
    (5, 'Thứ 7'),
    (6, 'Chủ nhật'),
]

APPOINTMENT_PENDING_EMAIL = 'pending_email'
APPOINTMENT_PENDING_PAYMENT = 'pending_payment'
APPOINTMENT_CONFIRMED = 'confirmed'
APPOINTMENT_COMPLETED = 'completed'
APPOINTMENT_CANCELLED = 'cancelled'
APPOINTMENT_NO_SHOW = 'no_show'

APPOINTMENT_STATUS_CHOICES = [
    (APPOINTMENT_PENDING_EMAIL, 'Chờ xác nhận email'),
    (APPOINTMENT_PENDING_PAYMENT, 'Chờ thanh toán'),
    (APPOINTMENT_CONFIRMED, 'Đã xác nhận'),
    (APPOINTMENT_COMPLETED, 'Đã khám'),
    (APPOINTMENT_CANCELLED, 'Đã hủy'),
    (APPOINTMENT_NO_SHOW, 'Không đến khám'),
]

PAYMENT_UNPAID = 'unpaid'
PAYMENT_PAID = 'paid'
PAYMENT_FAILED = 'failed'
PAYMENT_CANCELLED = 'cancelled'
PAYMENT_STATUS_CHOICES = [
    (PAYMENT_UNPAID, 'Chưa thanh toán'),
    (PAYMENT_PAID, 'Đã thanh toán'),
    (PAYMENT_FAILED, 'Thanh toán thất bại'),
    (PAYMENT_CANCELLED, 'Đã hủy thanh toán'),
]
