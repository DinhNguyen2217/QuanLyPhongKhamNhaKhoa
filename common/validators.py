import re
from django.core.exceptions import ValidationError

PHONE_REGEX = re.compile(r'^(0|\+84)\d{9,10}$')


def validate_vietnam_phone(value):
    if not PHONE_REGEX.match(value or ''):
        raise ValidationError('Số điện thoại không hợp lệ. Ví dụ: 0912345678')
