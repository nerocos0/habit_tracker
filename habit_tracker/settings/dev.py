from .base import *

DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME' : os.getenv('NAME'),
        'USER' : os.getenv('USER'),
        'PASSWORD' : os.getenv('PASSWORD'),
        'HOST' : os.getenv('HOST'),
        'PORT' : os.getenv('PORT'),
        'ATOMIC_REQUESTS' : True
    }
}