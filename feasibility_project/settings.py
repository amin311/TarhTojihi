import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1234567890!@#$%^&*()_+example'
DEBUG = True
ALLOWED_HOSTS = []

# تعریف پایگاه داده SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# اپلیکیشن‌های نصب‌شده (Installed Apps)
INSTALLED_APPS = [
    # Django Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # جانبی
    'rest_framework',
    'corsheaders',
    'django_jalali',

    # سفارشی (اپلیکیشن‌های پروژه)
    'apps.users',
    'apps.categories',
    'apps.expenses',
    'apps.projects',
    'apps.energy_fuel_prices',
    'apps.recommendations',
    'apps.finance',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # فعال‌سازی پشتیبانی از زبان
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'feasibility_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # مسیر پوشه templates
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

WSGI_APPLICATION = 'feasibility_project.wsgi.application'

# زبان و منطقه زمانی برای فارسی‌سازی
LANGUAGE_CODE = 'fa-ir'

LANGUAGES = [
    ('fa', _('Persian')),
]

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True
USE_L10N = False  # به دلیل استفاده از تقویم شمسی معمولاً غیرفعال می‌شود
USE_TZ = True

# برای پشتیبانی از تقویم شمسی
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# در صورت نیاز به مدل کاربری سفارشی
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

CORS_ALLOW_ALL_ORIGINS = True  # توسعه محلی: اجازه همه Origin‌ها
# در صورت نیاز به محدودیت، از CORS_ALLOWED_ORIGINS استفاده کنید
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:5174',
]
CORS_ALLOW_CREDENTIALS = False

# پایان فایل settings.py
