from django.contrib.auth.decorators import user_passes_test
from .choices import ROLE_ADMIN, ROLE_DOCTOR, ROLE_CUSTOMER


def role_required(role):
    return user_passes_test(lambda u: u.is_authenticated and u.role == role)

admin_required = role_required(ROLE_ADMIN)
doctor_required = role_required(ROLE_DOCTOR)
customer_required = role_required(ROLE_CUSTOMER)
