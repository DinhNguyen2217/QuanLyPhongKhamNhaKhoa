from random import choice

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone

from common.choices import (
    APPOINTMENT_CONFIRMED,
    APPOINTMENT_COMPLETED,
    APPOINTMENT_PENDING_EMAIL,
    APPOINTMENT_PENDING_PAYMENT,
    PAYMENT_CANCELLED,
    PAYMENT_FAILED,
    PAYMENT_PAID,
)
from apps.doctors.models import Doctor
from .models import Appointment, PaymentTransaction


class BookingError(Exception):
    pass


BOOKED_STATUSES = [
    APPOINTMENT_PENDING_EMAIL,
    APPOINTMENT_PENDING_PAYMENT,
    APPOINTMENT_CONFIRMED,
    APPOINTMENT_COMPLETED,
]
MAX_PATIENTS_PER_DOCTOR_SHIFT = 5
MAX_PATIENTS_PER_SHIFT = 10


def _doctor_queryset(service, appointment_date, shift):
    weekday = appointment_date.weekday()
    return (
        Doctor.objects.filter(
            services=service,
            schedules__weekday=weekday,
            schedules__shift=shift,
            schedules__is_active=True,
        )
        .distinct()
        .annotate(
            booked_count=Count(
                'appointments',
                filter=Q(appointments__appointment_date=appointment_date)
                & Q(appointments__shift=shift)
                & Q(appointments__status__in=BOOKED_STATUSES),
            )
        )
        .order_by('booked_count', 'full_name', 'user__username')
    )


def get_doctor_availability(service, appointment_date, shift):
    if not service or not appointment_date or not shift:
        return []
    doctors = []
    for doctor in _doctor_queryset(service, appointment_date, shift):
        booked = doctor.booked_count or 0
        doctors.append({
            'id': doctor.pk,
            'name': doctor.display_name,
            'doctor': doctor,
            'services': ', '.join(doctor.services.values_list('name', flat=True)),
            'booked_count': booked,
            'capacity': MAX_PATIENTS_PER_DOCTOR_SHIFT,
            'remaining': max(MAX_PATIENTS_PER_DOCTOR_SHIFT - booked, 0),
            'available': booked < MAX_PATIENTS_PER_DOCTOR_SHIFT,
        })
    return doctors


def get_selectable_doctors(service, appointment_date, shift):
    return [item['doctor'] for item in get_doctor_availability(service, appointment_date, shift) if item['available']]


def choose_doctor_for_appointment(service, appointment_date, shift, selected_doctor=None):
    doctors_info = get_doctor_availability(service, appointment_date, shift)
    available = [item for item in doctors_info if item['available']]
    if not doctors_info:
        raise BookingError('Ngày và ca này không có bác sĩ thuộc dịch vụ đã chọn.')
    if not available:
        raise BookingError('Tất cả bác sĩ của dịch vụ này đã kín lịch. Vui lòng chọn ngày hoặc ca khác.')

    active_appointments = Appointment.objects.filter(
        appointment_date=appointment_date,
        shift=shift,
        status__in=BOOKED_STATUSES,
    ).count()
    total_capacity = min(MAX_PATIENTS_PER_SHIFT, len(doctors_info) * MAX_PATIENTS_PER_DOCTOR_SHIFT)
    if active_appointments >= total_capacity:
        raise BookingError('Ca khám đã đạt giới hạn tiếp nhận. Vui lòng chọn ngày hoặc ca khác.')

    if selected_doctor:
        chosen = next((item for item in doctors_info if item['doctor'].pk == selected_doctor.pk), None)
        if not chosen:
            raise BookingError('Bác sĩ đã chọn không thuộc dịch vụ hoặc không làm việc ở ca này.')
        if not chosen['available']:
            raise BookingError('Bác sĩ đã chọn đã kín lịch. Vui lòng chọn bác sĩ khác.')
        return selected_doctor

    return choice(available)['doctor']


def create_booking(user, cleaned_data):
    service = cleaned_data['service']
    appointment_date = cleaned_data['appointment_date']
    shift = cleaned_data['shift']
    selected_doctor = cleaned_data.get('doctor') if cleaned_data.get('assignment_mode') == 'manual' else None
    doctor = choose_doctor_for_appointment(service, appointment_date, shift, selected_doctor)

    appointment = Appointment.objects.create(
        customer=user,
        doctor=doctor,
        service=service,
        full_name=cleaned_data['full_name'],
        email=cleaned_data['email'],
        phone=cleaned_data['phone'],
        gender=cleaned_data['gender'],
        symptom=cleaned_data.get('symptom', ''),
        appointment_date=appointment_date,
        shift=shift,
        deposit_amount=100000,
    )
    PaymentTransaction.objects.create(
        appointment=appointment,
        amount=appointment.deposit_amount,
    )
    send_confirmation_email(appointment)
    return appointment


def send_confirmation_email(appointment):
    confirm_url = settings.SITE_BASE_URL + reverse('appointments:confirm_email', args=[str(appointment.email_token)])
    subject = 'Xác nhận đặt lịch khám nha khoa'
    text_content = (
        f"Xin chào {appointment.full_name},\n\n"
        f"Bạn vừa tạo yêu cầu đặt lịch khám dịch vụ: {appointment.service.name}\n"
        f"Ngày khám: {appointment.appointment_date} - {appointment.get_shift_display()}\n"
        f"Bác sĩ dự kiến: {appointment.doctor}\n\n"
        f"Vui lòng bấm link sau để xác nhận lịch hẹn:\n{confirm_url}\n\n"
        "Nếu bạn không thực hiện yêu cầu này, hãy bỏ qua email."
    )
    html_content = f"""
    <html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #0f172a;">
        <div style="max-width:680px;margin:0 auto;padding:24px;">
            <h2 style="margin:0 0 12px;">Xác nhận đặt lịch khám nha khoa</h2>
            <p>Xin chào <strong>{appointment.full_name}</strong>,</p>
            <p>Bạn vừa tạo yêu cầu đặt lịch khám dịch vụ <strong>{appointment.service.name}</strong>.</p>
            <p>Ngày khám: <strong>{appointment.appointment_date}</strong><br>Buổi khám: <strong>{appointment.get_shift_display()}</strong><br>Bác sĩ dự kiến: <strong>{appointment.doctor}</strong></p>
            <p style="margin:24px 0;"><a href="{confirm_url}" style="display:inline-block;padding:12px 20px;background:#16a34a;color:#fff;text-decoration:none;border-radius:8px;font-weight:bold;">Xác nhận lịch hẹn</a></p>
            <p>Nếu nút không bấm được, dùng link sau:</p>
            <p><a href="{confirm_url}">{confirm_url}</a></p>
        </div>
    </body></html>
    """
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[appointment.email],
    )
    email.attach_alternative(html_content, 'text/html')
    try:
        email.send(fail_silently=False)
    except Exception as e:
        print('EMAIL ERROR:', e)


def mark_email_confirmed(appointment):
    appointment.status = APPOINTMENT_PENDING_PAYMENT
    appointment.save(update_fields=['status'])


def handle_payment_result(appointment, result, method=None):
    payment = appointment.payment
    if method:
        payment.method = method
    if result == 'success':
        appointment.status = APPOINTMENT_CONFIRMED
        appointment.payment_status = PAYMENT_PAID
        payment.status = PAYMENT_PAID
        payment.paid_at = timezone.now()
    elif result == 'failed':
        appointment.payment_status = PAYMENT_FAILED
        payment.status = PAYMENT_FAILED
    else:
        appointment.payment_status = PAYMENT_CANCELLED
        payment.status = PAYMENT_CANCELLED
    appointment.save(update_fields=['status', 'payment_status'])
    payment.save(update_fields=['status', 'paid_at', 'method'])
