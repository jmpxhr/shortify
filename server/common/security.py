from datetime import timedelta
from typing import ClassVar

from django.conf import settings
from django_stubs_ext import StrOrPromise
from dmr.cookies import SameSite


# TODO: move to ?
class JWTCookieSettings:
    """Cookie settings shared by all auth controllers."""

    jwt_access_cookie: ClassVar[str] = settings.ACCESS_COOKIE_NAME
    jwt_refresh_cookie: ClassVar[str] = settings.REFRESH_COOKIE_NAME
    jwt_refresh_cookie_path: ClassVar[StrOrPromise | None] = (
        settings.REFRESH_COOKIE_PATH
    )
    jwt_expiration: ClassVar[timedelta] = settings.JWT_ACCESS_TTL
    jwt_refresh_expiration: ClassVar[timedelta] = settings.JWT_REFRESH_TTL
    jwt_cookie_secure: ClassVar[bool] = True
    jwt_cookie_httponly: ClassVar[bool] = settings.JWT_COOKIE_HTTPONLY
    jwt_cookie_samesite: ClassVar[SameSite] = settings.JWT_COOKIE_SAMESITE
