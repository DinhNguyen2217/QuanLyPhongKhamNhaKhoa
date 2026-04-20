from django import forms
from .models import PriceItem, Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'


class PriceItemForm(forms.ModelForm):
    class Meta:
        model = PriceItem
        fields = '__all__'
