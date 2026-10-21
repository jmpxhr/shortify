"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""

from django.core.exceptions import ImproperlyConfigured
from dmr.settings import Settings

from server.settings.components import config
from server.settings.components.api import DMR_SETTINGS
from server.settings.components.common import SECRET_KEY

# Refuse to boot with the insecure development fallback secret key:
if SECRET_KEY.startswith('django-insecure-'):
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY in production!')

# Production flags:
# https://docs.djangoproject.com/en/6.0/howto/deployment/

DEBUG = False

ALLOWED_HOSTS = [
    # TODO: check production hosts
    config('DOMAIN_NAME'),
    # We need this value for `healthcheck` to work:
    'localhost',
]


# Staticfiles
# https://docs.djangoproject.com/en/6.0/ref/contrib/staticfiles/

# This is a hack to allow a special flag to be used with `--dry-run`
# to test things locally.
_COLLECTSTATIC_DRYRUN = config(
    'DJANGO_COLLECTSTATIC_DRYRUN',
    cast=bool,
    default=False,
)
# Adding STATIC_ROOT to collect static files via 'collectstatic':
STATIC_ROOT = '.static' if _COLLECTSTATIC_DRYRUN else '/var/www/django/static'

# TODO: convert to `STORAGES`
STATICFILES_STORAGE = (
    # This is a string, not a tuple,
    # but it does not fit into 80 characters rule.
    'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
)


# Media files
# https://docs.djangoproject.com/en/6.0/topics/files/

MEDIA_ROOT = '/var/www/django/media'


# Security
# https://docs.djangoproject.com/en/6.0/topics/security/

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# django-modern-rest
# https://django-modern-rest.rtfd.io

DMR_SETTINGS[Settings.validate_responses] = False
