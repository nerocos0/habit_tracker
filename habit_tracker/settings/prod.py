from .base import *

DEBUG=False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME' : os.getenv('POSTGRES_DB'),
        'USER' : os.getenv('POSTGRES_USER'),
        'PASSWORD' : os.getenv('POSTGRES_PASSWORD'),
        'HOST' : os.getenv('POSTGRES_HOST'),
        'PORT' : os.getenv('POSTGRES_PORT'),
        'ATOMIC_REQUESTS' : True
    }
}

# HTTPS за прокси
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# автоперенаправление с HTTP на HTTPS по этому домену
# 60 секунд значат что брауер запомнит на 60 секунд что именно по этому домену делать только HTTPS запросы
# в течение 60 секунд невозможно будет зайти на сайт если что нибудь сломается в HTTPS
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True