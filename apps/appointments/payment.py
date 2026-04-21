import base64
from io import BytesIO

import qrcode
from django.conf import settings
from django.urls import reverse


def build_qr_base64(qr_text: str) -> str:
    if not qr_text:
        return ''
    img = qrcode.make(qr_text)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


def create_internal_payment(appointment):
    payment = appointment.payment
    token = str(payment.transaction_code)
    pay_url = settings.QR_BASE_URL + reverse('appointments:fake_gateway', args=[token])
    qr_image = build_qr_base64(pay_url)
    return {
        'pay_url': pay_url,
        'qr_image': qr_image,
        'order_id': token,
    }
