from django.shortcuts import render
from apps.catalog.models import PriceItem, Service
from apps.doctors.models import Doctor


def home_view(request):
    services = Service.objects.all()[:6]
    doctors = Doctor.objects.select_related('user').all()[:4]
    return render(request, 'core/home.html', {'services': services, 'doctors': doctors})


def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    return render(request, 'core/contact.html')


def pricing_view(request):
    prices = PriceItem.objects.select_related('service').all()
    return render(request, 'core/pricing.html', {'prices': prices})
