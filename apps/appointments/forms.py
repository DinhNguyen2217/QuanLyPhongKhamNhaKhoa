from datetime import date
from django import forms
from django.utils import timezone
from apps.doctors.models import Doctor
from apps.catalog.models import Service
from .models import Appointment
from .services import get_selectable_doctors


ASSIGNMENT_CHOICES = [
    ('random', 'Hệ thống sắp xếp ngẫu nhiên'),
    ('manual', 'Tự chọn bác sĩ'),
]


class AppointmentForm(forms.ModelForm):
    assignment_mode = forms.ChoiceField(
        choices=ASSIGNMENT_CHOICES,
        initial='random',
        label='Cách sắp xếp bác sĩ',
        widget=forms.RadioSelect,
    )
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        required=False,
        label='Chọn bác sĩ',
        empty_label='Hãy chọn bác sĩ',
    )

    class Meta:
        model = Appointment
        fields = ['full_name', 'email', 'phone', 'gender', 'service', 'appointment_date', 'shift', 'assignment_mode', 'doctor', 'symptom']
        labels = {
            'symptom': 'Ghi chú',
        }
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'symptom': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Mô tả tình trạng hoặc ghi chú thêm'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.RadioSelect):
                continue
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['data-label'] = field.label
            if field.required:
                field.widget.attrs['required'] = 'required'
        self.fields['phone'].widget.attrs.update({'pattern': r'^(0|\+84)\d{9,10}$', 'inputmode': 'numeric'})
        self.fields['full_name'].widget.attrs.update({'maxlength': '120'})
        self.fields['doctor'].widget.attrs['class'] = 'form-select'

        service = None
        appointment_date = None
        raw = self.data if self.is_bound else self.initial
        service_id = raw.get('service')
        date_value = raw.get('appointment_date')
        shift = raw.get('shift')
        if service_id:
            try:
                service = Service.objects.get(pk=service_id)
            except (Service.DoesNotExist, ValueError, TypeError):
                service = None
        if date_value:
            try:
                appointment_date = date.fromisoformat(str(date_value))
            except ValueError:
                appointment_date = None
        if service and appointment_date and shift:
            self.fields['doctor'].queryset = Doctor.objects.filter(pk__in=[d.pk for d in get_selectable_doctors(service, appointment_date, shift)])

    def clean_appointment_date(self):
        value = self.cleaned_data['appointment_date']
        if value < timezone.localdate():
            raise forms.ValidationError('Ngày khám không được nhỏ hơn ngày hiện tại.')
        return value

    def clean(self):
        cleaned = super().clean()
        service = cleaned.get('service')
        appointment_date = cleaned.get('appointment_date')
        shift = cleaned.get('shift')
        doctor = cleaned.get('doctor')
        assignment_mode = cleaned.get('assignment_mode')
        if service and appointment_date and shift and assignment_mode == 'manual' and not doctor:
            self.add_error('doctor', 'Vui lòng chọn bác sĩ còn trống lịch.')
        return cleaned
