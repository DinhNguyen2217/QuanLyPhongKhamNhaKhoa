from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Quản trị phòng khám nha khoa'
admin.site.site_title = 'Admin phòng khám'
admin.site.index_title = 'Bảng điều khiển quản trị'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('catalog/', include('apps.core.placeholder_catalog_urls')),
    path('doctors/', include('apps.doctors.urls')),
    path('appointments/', include('apps.core.placeholder_appointments_urls')),
    path('dashboard/', include('apps.core.placeholder_dashboard_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
