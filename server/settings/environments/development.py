import socket

from server.settings.components import config
from server.settings.components.common import (
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
)
from server.settings.components.cors import (
    CORS_ALLOWED_ORIGINS,
    CSRF_TRUSTED_ORIGINS,
)

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS: list[str] = [
    config('DOMAIN_NAME', default='localhost'),
    'localhost',
    '0.0.0.0',  # ruff: ignore[hardcoded-bind-all-interfaces]
    '127.0.0.1',
    '[::1]',
]

# Installed apps for development only:

INSTALLED_APPS += (
    # Better debug:
    'debug_toolbar',
)

# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        '{}.1'.format(ip[: ip.rfind('.')])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except OSError:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ['127.0.0.1', '10.0.2.2']

# django-cors-headers

_DEV_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]
CORS_ALLOWED_ORIGINS.extend(_DEV_ORIGINS)
CSRF_TRUSTED_ORIGINS.extend(_DEV_ORIGINS)

# Disable persistent DB connections
# https://docs.djangoproject.com/en/6.0/ref/databases/#caveats
DATABASES['default']['CONN_MAX_AGE'] = 0
