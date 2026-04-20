from django.contrib import admin
from .models import PriceItem, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active')
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'service', 'price', 'unit')
    search_fields = ('item_name', 'service__name')
