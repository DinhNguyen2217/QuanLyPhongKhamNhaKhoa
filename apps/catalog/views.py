from django.shortcuts import get_object_or_404, render
from .models import Service


def service_list_view(request):
    services = Service.objects.filter(is_active=True)
    return render(request, 'catalog/service_list.html', {'services': services})


def service_detail_view(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'catalog/service_detail.html', {'service': service})



