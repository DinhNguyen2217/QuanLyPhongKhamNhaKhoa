from django.urls import path
from .views import about_view, contact_view, home_view, pricing_view

app_name = 'core'

urlpatterns = [
    path('', home_view, name='home'),
    path('gioi-thieu/', about_view, name='about'),
    path('lien-he/', contact_view, name='contact'),
    path('bang-gia/', pricing_view, name='pricing'),
]
