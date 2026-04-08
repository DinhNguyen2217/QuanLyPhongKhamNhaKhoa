import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-tuy-bien-chu-oi'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appointments',
]

# ĐÂY LÀ PHẦN BẠN ĐANG THIẾU
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# KẾT NỐI MYSQL WORKBENCH
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'doan_db',
        'USER': 'root',
<<<<<<< HEAD
        'PASSWORD': '292004', # Mật khẩu bạn đã sửa thành root
=======
        'PASSWORD': 'nguyen2217', # Mật khẩu bạn đã sửa thành root
>>>>>>> d3a8a7475baba86de2855f00336c928707d882be
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Fix lỗi Warning về Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Cấu hình Static files (CSS, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Cấu hình gửi Email qua Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lam_2251220242@dau.edu.vn' # Email nhận thông báo
EMAIL_HOST_PASSWORD = 'zfnhaaifzrwjlonu' # Mật khẩu ứng dụng Gmail

# ...existing code...
# Override sensitive values from environment if present (recommended)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', EMAIL_HOST_PASSWORD)

# Ngôn ngữ / timezone
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Kiểm soát mật khẩu (production)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Static & Media (deploy)
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Auth redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Dev hint: if you plan to build API add DRF
# INSTALLED_APPS += ['rest_framework']