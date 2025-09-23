from .base import *
import os

DEBUG = False

MEDIA_ROOT = os.getenv('MEDIA_ROOT')
MEDIA_URL = os.getenv('MEDIA_URL')
STATIC_ROOT = os.getenv('STATIC_ROOT')
STATIC_URL = os.getenv('STATIC_URL')

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "https://queerlit.dh.gu.se/om"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
    }
}

try:
    from .local import *
except ImportError:
    pass
