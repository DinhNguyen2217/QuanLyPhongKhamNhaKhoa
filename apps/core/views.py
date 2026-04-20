from django.shortcuts import render
from apps.catalog.models import PriceItem


def home_view(request):
    return render(request, 'core/home.html')


def about_view(request):
    return render(request, 'core/about.html')


def contact_view(request):
    return render(request, 'core/contact.html')


def pricing_view(request):
    prices = PriceItem.objects.select_related('service').all()
    return render(request, 'core/pricing.html', {'prices': prices})
