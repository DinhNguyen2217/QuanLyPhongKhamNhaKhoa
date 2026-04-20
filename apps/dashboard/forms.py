from django import forms
from apps.catalog.models import Service

WEEKDAYS = [
    (0, 'Thứ 2'), (1, 'Thứ 3'), (2, 'Thứ 4'), (3, 'Thứ 5'),
    (4, 'Thứ 6'), (5, 'Thứ 7'), (6, 'Chủ nhật'),
]
SHIFTS = [('morning', 'Ca sáng'), ('afternoon', 'Ca chiều')]


class ServiceScheduleBulkForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Khoa / Dịch vụ')
    weekdays = forms.MultipleChoiceField(
        choices=WEEKDAYS,
        widget=forms.CheckboxSelectMultiple,
        label='Chọn thứ trong tuần',
    )
    shifts = forms.MultipleChoiceField(
        choices=SHIFTS,
        widget=forms.CheckboxSelectMultiple,
        label='Chọn ca làm việc',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].widget.attrs['class'] = 'form-select'
