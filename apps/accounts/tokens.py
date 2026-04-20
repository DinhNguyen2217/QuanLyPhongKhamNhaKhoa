from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AppointmentEmailTokenGenerator(PasswordResetTokenGenerator):
    pass


appointment_email_token = AppointmentEmailTokenGenerator()
