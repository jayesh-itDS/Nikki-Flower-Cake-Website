from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y8zd1l_8-&+84)-u_@gsaq7!ga6=!6lk+e8mzajv(qwg*ymy+a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'nikki-flower-cake-ygrc.onrender.com'
]

# Development-specific apps
INSTALLED_APPS += [
    'apps.core',
    'apps.products',
    'apps.users',
    'apps.cart',
    'apps.orders',
    'apps.payments',
    'apps.recommendations',
    'apps.analytics',
    'apps.marketing',
    'apps.admin_dashboard',
]

# Development middleware
MIDDLEWARE += [
]

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar settings disabled

# Cache configuration for development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# HTMX settings
HTMX_ENABLED = True