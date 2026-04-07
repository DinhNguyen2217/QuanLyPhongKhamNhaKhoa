import os
from django.core.wsgi import get_wsgi_application

# Nhớ để là backend.settings vì thư mục của bạn tên là backend
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()