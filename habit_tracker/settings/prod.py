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