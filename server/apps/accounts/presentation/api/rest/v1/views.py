from http import HTTPStatus
from typing import final, override

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.debug import (
    sensitive_post_parameters,
    sensitive_variables,
)
from dmr import Controller, NewCookie, ResponseSpec, modify
from dmr.decorators import endpoint_decorator
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import BodyMsgspec, MsgspecSerializer
from dmr.security import AuthenticatedHttpRequest
from dmr.security.base import NO_STORE_HEADERS
from dmr.security.jwt.views import (
    CookieLogoutSyncController,
    CookieObtainTokensSyncController,
    CookieRefreshTokensSyncController,
)

from server.apps.accounts.application import use_cases
from server.apps.accounts.application.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    WeakPasswordError,
)
from server.apps.accounts.domain.exceptions import UserValidationError
from server.apps.accounts.presentation.api.rest.v1.mappers import (
    UserPresentationMapper,
)
from server.apps.accounts.presentation.api.rest.v1.schemas import (
    ObtainTokensPayload,
    SignUpSchema,
    UserResponseSchema,
    UserUpdateSchema,
)
from server.common.di import HasContainer
from server.common.security import JWTCookieSettings


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
class CurrentUserView(HasContainer, Controller[MsgspecSerializer]):
    """Read, update, or delete the authenticated user's profile."""

    description = 'Current user profile.'
    request: AuthenticatedHttpRequest[User]  # pyrefly: ignore [bad-override-mutable-attribute]

    def get(self) -> UserResponseSchema:
        """Return the current user's profile."""
        user_dto = self.resolve(use_cases.GetCurrentUser)(
            user_id=self.request.user.pk,
        )
        return self.resolve(UserPresentationMapper)(user=user_dto)

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
    )
    def patch(self, parsed_body: BodyMsgspec[UserUpdateSchema]) -> UserResponseSchema:
        """Update the current user's profile."""
        user_dto = self.resolve(use_cases.UpdateCurrentUser)(
            user_id=self.request.user.pk,
            username=parsed_body.username,
            email=parsed_body.email,
        )
        return self.resolve(UserPresentationMapper)(user=user_dto)

    @modify(
        status_code=HTTPStatus.NO_CONTENT,
        cookies={
            settings.ACCESS_COOKIE_NAME: NewCookie(
                value='',
                max_age=0,
                path='/',
            ),
            settings.REFRESH_COOKIE_NAME: NewCookie(
                value='',
                max_age=0,
                path=settings.REFRESH_COOKIE_PATH,
            ),
        },
    )
    def delete(self) -> None:
        """Delete the current user's account."""
        self.resolve(use_cases.DeleteCurrentUser)(
            user_id=self.request.user.pk,
        )

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, UserNotFoundError):
            return self.to_error(
                self.format_error(
                    'User not found',
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )

        if isinstance(exc, UserAlreadyExistsError):
            return self.to_error(
                self.format_error(
                    'User with this username already exists',
                    error_type=ErrorType.user_msg,
                ),
                status_code=HTTPStatus.CONFLICT,
            )

        if isinstance(exc, UserValidationError):
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
        """Convert the login schema to Django's credentials payload."""
        return {
            'username': payload['username'],
            'password': payload['password'],
        }


@final
class RefreshView(
    _ConfiguredJWTCookieSettings,
    CookieRefreshTokensSyncController[MsgspecSerializer],
):
    """Rotate the access and refresh cookies."""

    auth = None
    description = 'Refresh the JWT cookies.'


@final
class VerifyView(Controller[MsgspecSerializer]):
    """Check that the access token cookie is still valid."""

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
