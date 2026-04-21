from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.shortcuts import redirect
from apps.appointments.models import Appointment
from .services import mark_email_confirmed

from common.choices import PAYMENT_PAID, ROLE_CUSTOMER
from .forms import AppointmentForm
from .models import Appointment, PaymentTransaction
from .payment import create_internal_payment
from .services import BookingError, create_booking, get_doctor_availability, handle_payment_result, mark_email_confirmed


@login_required
def book_appointment_view(request):
    if request.user.role != ROLE_CUSTOMER:
        messages.error(request, 'Chỉ khách hàng mới có thể đặt lịch.')
        return redirect('core:home')
    initial = {
        'full_name': getattr(getattr(request.user, 'customer_profile', None), 'full_name', request.user.get_full_name() or request.user.username),
        'email': request.user.email,
        'phone': request.user.phone,
        'assignment_mode': 'random',
    }
    form = AppointmentForm(request.POST or None, initial=initial)
    availability_cards = []
    if form.is_bound and request.POST.get('service') and request.POST.get('appointment_date') and request.POST.get('shift') and form['service'].value():
        try:
            service = form.fields['service'].queryset.get(pk=form['service'].value())
            appointment_date = form.fields['appointment_date'].clean(request.POST.get('appointment_date'))
            shift = request.POST.get('shift')
            availability_cards = get_doctor_availability(service, appointment_date, shift)
        except Exception:
            availability_cards = []
    if request.method == 'POST' and form.is_valid():
        try:
            appointment = create_booking(request.user, form.cleaned_data)
            messages.success(request, 'Đặt lịch thành công. Vui lòng kiểm tra email để xác nhận lịch hẹn.')
            return redirect('appointments:booking_created', pk=appointment.pk)
        except BookingError as exc:
            form.add_error(None, str(exc))
    return render(request, 'appointments/book.html', {'form': form, 'availability_cards': availability_cards})


@login_required
def doctor_availability_view(request):
    if request.user.role != ROLE_CUSTOMER:
        return JsonResponse({'items': []})
    service_id = request.GET.get('service')
    appointment_date = request.GET.get('appointment_date')
    shift = request.GET.get('shift')
    form = AppointmentForm(initial={'service': service_id, 'appointment_date': appointment_date, 'shift': shift})
    try:
        service = form.fields['service'].queryset.get(pk=service_id)
        appointment_date = form.fields['appointment_date'].clean(appointment_date)
    except Exception:
        return JsonResponse({'items': []})
    items = [
        {
            'id': item['id'],
            'name': item['name'],
            'booked': item['booked_count'],
            'capacity': item['capacity'],
            'available': item['available'],
            'services': item['services'],
        }
        for item in get_doctor_availability(service, appointment_date, shift)
    ]
    return JsonResponse({'items': items})


@login_required
def booking_created_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user)
    return render(request, 'appointments/booking_created.html', {'appointment': appointment})


from django.shortcuts import render
from .models import Appointment

def confirm_email_view(request, token):
    appointment = Appointment.objects.filter(email_token=token).first()

    if not appointment:
        return render(request, 'appointments/email_confirm_result.html', {
            'success': False,
            'title': 'Xác nhận thất bại',
            'message': 'LIÊN KẾT XÁC NHẬN KHÔNG HỢP LỆ HOẶC ĐÃ HẾT HẠN',
        })

    if appointment.status == "confirmed":
        return render(request, 'appointments/email_confirm_result.html', {
            'success': True,
            'title': 'Đã xác nhận trước đó',
            'message': 'LỊCH HẸN NÀY ĐÃ ĐƯỢC XÁC NHẬN TRƯỚC ĐÓ',
            'appointment': appointment,
        })

    mark_email_confirmed(appointment)

    return render(request, 'appointments/email_confirm_result.html', {
        'success': True,
        'title': 'Xác nhận thành công',
        'message': 'LỊCH HẸN ĐÃ ĐƯỢC XÁC NHẬN\nVUI LÒNG QUAY LẠI WEBSITE',
        'appointment': appointment,
    })

@login_required
def payment_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user)

    if appointment.status not in ['pending_payment', 'confirmed', 'completed']:
        messages.warning(request, 'Bạn cần xác nhận email trước khi thanh toán.')
        return redirect('appointments:booking_created', pk=appointment.pk)

    if appointment.payment_status == PAYMENT_PAID:
        messages.success(request, 'Lịch hẹn này đã được thanh toán.')
        return redirect('appointments:history')

    payment_data = create_internal_payment(appointment)

    return render(request, 'appointments/payment.html', {
        'appointment': appointment,
        'payment_data': payment_data,
    })


@login_required
def payment_status_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, customer=request.user)
    return JsonResponse({
        'payment_status': appointment.payment_status,
        'appointment_status': appointment.status,
        'is_paid': appointment.payment_status == PAYMENT_PAID,
    })


def fake_gateway_view(request, token):
    payment = get_object_or_404(PaymentTransaction.objects.select_related('appointment__service'), transaction_code=token)
    return render(request, 'appointments/fake_gateway.html', {
        'payment': payment,
        'appointment': payment.appointment,
        'already_paid': payment.status == PAYMENT_PAID,
        'confirm_url': reverse('appointments:fake_gateway_confirm', args=[payment.transaction_code]),
        'success_url': reverse('appointments:history'),
    })


def fake_gateway_confirm_view(request, token):
    payment = get_object_or_404(PaymentTransaction.objects.select_related('appointment'), transaction_code=token)
    appointment = payment.appointment
    if payment.status != PAYMENT_PAID:
        handle_payment_result(appointment, 'success', method='qr_gateway')
    return render(request, 'appointments/fake_gateway_success.html', {
        'appointment': appointment,
    })


@login_required
def history_view(request):
    appointments = request.user.appointments.select_related('doctor__user', 'service').all()
    return render(request, 'appointments/history.html', {'appointments': appointments})
