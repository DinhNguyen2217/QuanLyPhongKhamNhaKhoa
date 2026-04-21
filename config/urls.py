from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = 'Quản trị phòng khám nha khoa'
admin.site.site_title = 'Admin phòng khám'
admin.site.index_title = 'Bảng điều khiển quản trị'
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('doctors/', include('apps.doctors.urls')),
    path('appointments/', include('apps.appointments.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
