from django.urls import path
from . import placeholder_views as views

app_name = 'catalog'

urlpatterns = [
    path('services/', views.catalog_service_list, name='service_list'),
    path('services/<slug:slug>/', views.catalog_service_detail, name='service_detail'),
]
