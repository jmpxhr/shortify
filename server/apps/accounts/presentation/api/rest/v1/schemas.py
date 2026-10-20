from typing import Annotated, final

import msgspec

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
        ),
    ]
    email: Annotated[
        str,
        msgspec.Meta(
            min_length=1,
            max_length=EMAIL_MAX_LENGTH,
            pattern=EMAIL_PATTERN,
        ),
    ]
    password: Annotated[
        str,
        msgspec.Meta(
            min_length=PASSWORD_MIN_LENGTH,
            max_length=PASSWORD_MAX_LENGTH,
        ),
    ]


@final
class UserResponseSchema(msgspec.Struct):
    """Schema for a user API response."""

    id: int
    username: str
    email: str
