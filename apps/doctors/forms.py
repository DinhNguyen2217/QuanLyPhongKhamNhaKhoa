from django import forms
from common.choices import SHIFT_CHOICES, WEEKDAY_CHOICES
from .models import Doctor


class AdminBulkDoctorScheduleForm(forms.Form):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.select_related('user').prefetch_related('services').order_by('full_name'),
        label='Bác sĩ',
        help_text='Chọn bác sĩ cần xếp lịch làm việc.',
    )
    weekdays = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Chọn nhiều ngày trong tuần',
    )
    shifts = forms.MultipleChoiceField(
        choices=SHIFT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Chọn ca làm việc',
    )
    replace_existing = forms.BooleanField(
        required=False,
        initial=False,
        label='Xóa lịch cũ của bác sĩ trước khi lưu',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].widget.attrs['class'] = 'vTextField admin-select-like'
