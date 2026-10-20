from datetime import timedelta
from typing import ClassVar, Final

from django.urls import reverse_lazy
from dmr.cookies import SameSite
from dmr.internal.types import StrOrPromise
from dmr.security.jwt import CookieJWTSyncAuth

ACCESS_COOKIE_NAME: Final = 'access_token'
REFRESH_COOKIE_NAME: Final = 'refresh_token'
REFRESH_COOKIE_PATH: Final = reverse_lazy('api:v1:refresh')

JWT_ACCESS_TTL: Final = timedelta(minutes=30)  # noqa: WPS432
JWT_REFRESH_TTL: Final = timedelta(days=14)  # noqa: WPS432

JWT_COOKIE_HTTPONLY: Final = True
JWT_COOKIE_SAMESITE: Final[SameSite] = 'lax'

jwt_cookie_auth = CookieJWTSyncAuth(
    cookie_name=ACCESS_COOKIE_NAME,
    security_scheme_name='jwt_cookie',
)


class JWTCookieSettings:
    """Cookie settings shared by all auth controllers."""

    jwt_access_cookie: ClassVar[str] = ACCESS_COOKIE_NAME
    jwt_refresh_cookie: ClassVar[str] = REFRESH_COOKIE_NAME
    jwt_refresh_cookie_path: ClassVar[StrOrPromise | None] = REFRESH_COOKIE_PATH
    jwt_expiration: ClassVar[timedelta] = JWT_ACCESS_TTL
    jwt_refresh_expiration: ClassVar[timedelta] = JWT_REFRESH_TTL
    # Secure by default. Environment-aware controllers override this
    # with ``not settings.DEBUG`` after the settings are loaded.
    jwt_cookie_secure: ClassVar[bool] = True
    jwt_cookie_httponly: ClassVar[bool] = JWT_COOKIE_HTTPONLY
    jwt_cookie_samesite: ClassVar[SameSite] = JWT_COOKIE_SAMESITE
