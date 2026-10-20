import tomllib
from datetime import timedelta
from typing import Final, cast

from django.urls import reverse_lazy
from dmr.cookies import SameSite
from dmr.openapi import OpenAPIConfig
from dmr.security.jwt import CookieJWTSyncAuth
from dmr.settings import SettingsDict

from server.settings.components import BASE_DIR


# TODO: Use static version?
def _get_project_meta() -> dict[str, str]:
    pyproject = BASE_DIR / 'pyproject.toml'
    return cast(
        dict[str, str],
        tomllib.loads(pyproject.read_text())['project'],
    )


ACCESS_TTL_IN_MINUTES: Final = 30
REFRESH_TTL_IN_DAYS: Final = 14

ACCESS_COOKIE_NAME: Final = 'access_token'
REFRESH_COOKIE_NAME: Final = 'refresh_token'
REFRESH_COOKIE_PATH: Final = reverse_lazy('api:v1:refresh')

JWT_ACCESS_TTL: Final = timedelta(minutes=ACCESS_TTL_IN_MINUTES)
JWT_REFRESH_TTL: Final = timedelta(days=REFRESH_TTL_IN_DAYS)

JWT_COOKIE_HTTPONLY: Final = True
JWT_COOKIE_SAMESITE: Final[SameSite] = 'lax'

jwt_cookie_auth = CookieJWTSyncAuth(
    cookie_name=ACCESS_COOKIE_NAME,
    security_scheme_name='jwt_cookie',
)

# django-modern-rest
# https://django-modern-rest.readthedocs.io

DMR_SETTINGS = SettingsDict(
    auth=[jwt_cookie_auth],
    openapi_config=OpenAPIConfig(
        title='Django Shortify',
        version=_get_project_meta()['version'],
    ),
)
