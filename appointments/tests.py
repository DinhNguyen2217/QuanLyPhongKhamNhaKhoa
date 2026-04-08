# ...existing code...
from django.test import TestCase
from .models import Appointment, Service, Doctor
from datetime import date

class AppointmentModelTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(name='Test Service', price=100000)
        self.doctor = Doctor.objects.create(name='Dr Test')
        self.date = date.today()

    def test_phone_validator_rejects_letters(self):
        with self.assertRaises(Exception):
            Appointment.objects.create(fullname='A', phone='abc123', date=self.date, shift='morning')

    def test_slot_limit_prevents_overbooking(self):
        max_per_shift = 3
        for i in range(max_per_shift):
            Appointment.create_with_slot_check(
                fullname=f'User{i}', phone='0901234567', date=self.date, shift='morning',
                service=self.service, doctor=self.doctor, deposit=0, max_per_shift=max_per_shift
            )
        with self.assertRaises(ValueError):
            Appointment.create_with_slot_check(
                fullname='UserX', phone='0901234567', date=self.date, shift='morning',
                service=self.service, doctor=self.doctor, deposit=0, max_per_shift=max_per_shift
            )
# ...existing code...