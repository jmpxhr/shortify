from server.settings.components import config

# django-cors-headers
# https://github.com/adamchainz/django-cors-headers


CORS_ALLOWED_ORIGINS = [
    f'https://{config("DOMAIN_NAME", default="localhost")}',
    f'https://{config("FRONTEND_URL", default="localhost:3000")}',
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_CREDENTIALS = True
