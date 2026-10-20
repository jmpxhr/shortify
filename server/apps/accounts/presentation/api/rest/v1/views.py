from http import HTTPStatus
from typing import final, override

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.debug import (
    sensitive_post_parameters,
    sensitive_variables,
)
from dmr import Controller, ResponseSpec, modify
from dmr.decorators import endpoint_decorator
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import BodyMsgspec, MsgspecSerializer
from dmr.security.base import NO_STORE_HEADERS
from dmr.security.jwt.views import (
    CookieLogoutSyncController,
    CookieObtainTokensSyncController,
    CookieRefreshTokensSyncController,
    ObtainTokensPayload,
)
from dmr.throttling import Rate, SyncThrottle
from dmr.throttling.cache_keys import RemoteAddr

from server.apps.accounts.application import use_cases
from server.apps.accounts.application.exceptions import (
    UserAlreadyExistsError,
    WeakPasswordError,
)
from server.apps.accounts.domain.exceptions import UserValidationError
from server.apps.accounts.presentation.api.rest.v1.mappers import (
    UserPresentationMapper,
)
from server.apps.accounts.presentation.api.rest.v1.schemas import (
    SignUpSchema,
    UserResponseSchema,
)
from server.common.di import HasContainer
from server.common.security import JWTCookieSettings, jwt_cookie_auth

_REFRESH_THROTTLE = SyncThrottle(
    10,
    Rate.minute,
    cache_key=RemoteAddr(),
)


class _ConfiguredJWTCookieSettings(JWTCookieSettings):
    """Apply cookie security based on the loaded environment."""

    jwt_cookie_secure = not settings.DEBUG


@final
class SignUpView(HasContainer, Controller[MsgspecSerializer]):
    """Register a new user account."""

    auth = None
    description = 'Sign up a new user.'

    @sensitive_variables()
    @endpoint_decorator(sensitive_post_parameters())
    @modify(
        extra_responses=[
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.BAD_REQUEST,
            ),
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.CONFLICT,
            ),
        ],
        throttling=[
            SyncThrottle(5, Rate.minute, cache_key=RemoteAddr()),
        ],
    )
    def post(self, parsed_body: BodyMsgspec[SignUpSchema]) -> UserResponseSchema:
        """Create a user with the given username, email, and password."""
        user_dto = self.resolve(use_cases.RegisterUser)(
            username=parsed_body.username,
            email=parsed_body.email,
            password=parsed_body.password,
        )
        return self.resolve(UserPresentationMapper)(user=user_dto)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, UserAlreadyExistsError):
            return self.to_error(
                self.format_error(
                    'User with this username already exists',
                    error_type=ErrorType.user_msg,
                ),
                status_code=HTTPStatus.CONFLICT,
            )

        if isinstance(exc, (WeakPasswordError, UserValidationError)):
            return self.to_error(
                self.format_error(
                    str(exc),
                    error_type=ErrorType.user_msg,
                ),
                status_code=HTTPStatus.BAD_REQUEST,
            )
        return super().handle_error(endpoint, controller, exc)


@final
class LoginView(
    _ConfiguredJWTCookieSettings,
    CookieObtainTokensSyncController[
        MsgspecSerializer,
        ObtainTokensPayload,
    ],
):
    """Authenticate a user and issue access and refresh cookies."""

    auth = None
    description = 'Log in and set the JWT cookies.'

    @override
    def convert_auth_payload(
        self,
        payload: ObtainTokensPayload,
    ) -> ObtainTokensPayload:
        """Use the default username and password payload."""
        return payload


@final
class RefreshView(
    _ConfiguredJWTCookieSettings,
    CookieRefreshTokensSyncController[MsgspecSerializer],
):
    """Rotate the access and refresh cookies."""

    auth = None
    description = 'Refresh the JWT cookies.'
    throttling = (_REFRESH_THROTTLE,)


@final
class VerifyView(Controller[MsgspecSerializer]):
    """Check that the access token cookie is still valid."""

    auth = (jwt_cookie_auth,)
    description = 'Verify the current access token.'

    @modify(
        status_code=HTTPStatus.NO_CONTENT,
        headers=NO_STORE_HEADERS,
    )
    def post(self) -> None:
        """Return an empty response when the access token is valid."""


@final
class LogoutView(
    _ConfiguredJWTCookieSettings,
    CookieLogoutSyncController[MsgspecSerializer],
):
    """Drop the JWT cookies."""

    auth = None
    description = 'Log out and clear the JWT cookies.'
