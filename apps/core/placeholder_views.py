from django.shortcuts import render
from django.http import JsonResponse


def placeholder_page(request, page_title, description):
    return render(request, 'core/module_placeholder.html', {
        'page_title': page_title,
        'description': description,
    })


def catalog_service_list(request):
    return placeholder_page(request, 'Danh sách dịch vụ', 'Chức năng dịch vụ và gói sản phẩm chưa được mở trong phiên bản hiện tại.')


def catalog_service_detail(request, slug):
    return placeholder_page(request, 'Chi tiết dịch vụ', 'Trang chi tiết dịch vụ sẽ xuất hiện khi module Dịch vụ được tích hợp.')


def doctors_list(request):
    return placeholder_page(request, 'Đội ngũ bác sĩ', 'Danh sách bác sĩ đang ở chế độ chờ phát triển trong phiên bản này.')


def doctors_detail(request, pk):
    return placeholder_page(request, 'Chi tiết bác sĩ', 'Trang chi tiết bác sĩ sẽ được thêm trong module Bác sĩ & lịch làm việc.')


def doctors_schedule(request):
    return placeholder_page(request, 'Lịch làm việc bác sĩ', 'Bảng lịch làm việc chung sẽ xuất hiện khi module Bác sĩ được kích hoạt.')


def doctors_portal(request):
    return placeholder_page(request, 'Cổng bác sĩ', 'Khu vực bác sĩ chưa được mở trong phiên bản hiện tại.')


def doctors_my_appointments(request):
    return placeholder_page(request, 'Lịch hẹn của bác sĩ', 'Danh sách lịch hẹn cho bác sĩ sẽ có trong bản tích hợp hoàn chỉnh.')


def appointments_book(request):
    return placeholder_page(request, 'Đặt lịch khám', 'Chức năng đặt lịch chưa được tích hợp trong phiên bản hiện tại.')


def appointments_created(request, pk):
    return placeholder_page(request, 'Kết quả tạo lịch', 'Màn hình kết quả đặt lịch sẽ có khi module Đặt lịch được kích hoạt.')


def appointments_history(request):
    return placeholder_page(request, 'Lịch sử đặt lịch', 'Lịch sử đặt lịch chưa khả dụng trong phiên bản hiện tại.')


def appointments_payment(request, pk):
    return placeholder_page(request, 'Thanh toán đặt cọc', 'Trang thanh toán sẽ có trong module Đặt lịch của thành viên phụ trách.')


def appointments_payment_status(request, pk):
    return JsonResponse({'status': 'inactive', 'message': 'Module thanh toán chưa kích hoạt.'})


def appointments_confirm_email(request, token):
    return placeholder_page(request, 'Xác nhận email lịch hẹn', 'Luồng xác nhận email chưa được bật trong phiên bản hiện tại.')


def appointments_availability(request):
    return JsonResponse({'items': [], 'message': 'Module đặt lịch chưa kích hoạt.'})


def appointments_fake_gateway(request, token):
    return placeholder_page(request, 'Cổng thanh toán giả lập', 'Cổng thanh toán giả lập chưa được bật trong phiên bản hiện tại.')


def appointments_fake_gateway_confirm(request, token):
    return placeholder_page(request, 'Xác nhận thanh toán giả lập', 'Chức năng xác nhận thanh toán giả lập chưa được bật trong phiên bản hiện tại.')


def dashboard_home(request):
    return placeholder_page(request, 'Dashboard quản trị', 'Bảng điều khiển quản trị sẽ được trưởng nhóm hoàn thiện ở bản cuối cùng.')


def dashboard_doctor_schedule(request):
    return placeholder_page(request, 'Quản lý lịch bác sĩ', 'Trang quản lý lịch bác sĩ sẽ được bật trong bản tích hợp cuối.')
