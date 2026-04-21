from django.urls import path
from .views import service_detail_view, service_list_view

app_name = 'catalog'

urlpatterns = [
    path('services/', service_list_view, name='service_list'),
    path('services/<slug:slug>/', service_detail_view, name='service_detail'),
    
]
