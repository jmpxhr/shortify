from server.settings.components import config

# django-cors-headers
# https://github.com/adamchainz/django-cors-headers


CORS_ALLOWED_ORIGINS = [
    f'https://{config("DOMAIN_NAME", default="localhost")}',
    f'https://{config("FRONTEND_URL", default="localhost:3000")}',
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

# django CSRF
# https://docs.djangoproject.com/en/6.0/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = [
    f'https://{config("DOMAIN_NAME", default="localhost")}',
    f'https://{config("FRONTEND_URL", default="localhost:3000")}',
]
