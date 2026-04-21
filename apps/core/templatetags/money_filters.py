from decimal import Decimal, InvalidOperation
from django import template

register = template.Library()


@register.filter
def vnd(value):
    if value in (None, ''):
        return '0 VNĐ'
    try:
        amount = int(Decimal(str(value)))
    except (InvalidOperation, ValueError, TypeError):
        return value
    formatted = f"{amount:,}".replace(',', '.')
    return f"{formatted} VNĐ"
