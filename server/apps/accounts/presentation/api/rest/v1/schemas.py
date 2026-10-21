from typing import Annotated, final

import msgspec
from dmr.security.jwt.views import ObtainTokensPayload as _DmrObtainTokensPayload

from server.apps.accounts.domain.constants import (
    EMAIL_MAX_LENGTH,
    EMAIL_PATTERN,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_PATTERN,
)


@final
class SignUpSchema(msgspec.Struct):
    username: Annotated[
        str,
        msgspec.Meta(
            min_length=1,
            max_length=USERNAME_MAX_LENGTH,
            pattern=USERNAME_PATTERN,
            examples=['johndoe'],
        ),
    ]
    email: Annotated[
        str,
        msgspec.Meta(
            min_length=1,
            max_length=EMAIL_MAX_LENGTH,
            pattern=EMAIL_PATTERN,
            examples=['john.doe@example.com'],
        ),
    ]
    password: Annotated[
        str,
        msgspec.Meta(
            min_length=PASSWORD_MIN_LENGTH,
            max_length=PASSWORD_MAX_LENGTH,
            examples=['strong-password-123'],
        ),
    ]


@final
class UserUpdateSchema(msgspec.Struct):
    """Schema for a partial current-user update."""

    username: (
        Annotated[
            str,
            msgspec.Meta(
                min_length=1,
                max_length=USERNAME_MAX_LENGTH,
                pattern=USERNAME_PATTERN,
                examples=['johndoe'],
            ),
        ]
        | None
    ) = None

    email: (
        Annotated[
            str,
            msgspec.Meta(
                min_length=1,
                max_length=EMAIL_MAX_LENGTH,
                pattern=EMAIL_PATTERN,
                examples=['john.doe@example.com'],
            ),
        ]
        | None
    ) = None


@final
class ObtainTokensPayload(_DmrObtainTokensPayload):
    """Schema for a login API request."""


@final
class UserResponseSchema(msgspec.Struct):
    """Schema for a user API response."""

    id: Annotated[int, msgspec.Meta(examples=[1])]
    username: Annotated[str, msgspec.Meta(examples=['johndoe'])]
    email: Annotated[str, msgspec.Meta(examples=['john.doe@example.com'])]
