from django.contrib.auth import get_user_model
from .models import CustomerProfile
from common.choices import ROLE_DOCTOR

User = get_user_model()


def ensure_doctor_user(username, email, full_name='Bác sĩ demo', phone='0912345678'):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'role': ROLE_DOCTOR,
            'phone': phone,
            'first_name': full_name,
        },
    )
    return user, created


def ensure_customer_profile(user):
    profile, _ = CustomerProfile.objects.get_or_create(
        user=user,
        defaults={'full_name': user.get_full_name() or user.username}
    )
    return profile
