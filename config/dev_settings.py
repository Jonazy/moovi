from config.base_settings import *
from pathlib import Path

from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = True
INSTALLED_APPS += [

]
DATABASES['default'].update({
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'PORT': 5432,
})

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIME': 5, # 5 seconds
    }

}

MEDIA_URL = '/uploaded/'
MEDIA_ROOT = BASE_DIR / 'media'