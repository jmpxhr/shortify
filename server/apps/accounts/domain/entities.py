import re
from dataclasses import dataclass
from typing import final

from server.apps.accounts.domain.constants import (
    EMAIL_MAX_LENGTH,
    EMAIL_PATTERN,
    USERNAME_MAX_LENGTH,
    USERNAME_PATTERN,
)
from server.apps.accounts.domain.exceptions import UserValidationError


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserEntity:
    id: int
    username: str
    email: str

    def __post_init__(self) -> None:
        """Validate entity fields after initialization."""
        self._validate_username()
        self._validate_email()

    def _validate_username(self) -> None:
        if re.match(USERNAME_PATTERN, self.username) is None:
            raise UserValidationError('username has an invalid format')

        if len(self.username) > USERNAME_MAX_LENGTH:
            raise UserValidationError(
                f'username is too long. Maximum allowed length is '
                f'{USERNAME_MAX_LENGTH} characters',
            )

    def _validate_email(self) -> None:
        if len(self.email) > EMAIL_MAX_LENGTH:
            raise UserValidationError(
                f'email is too long. Maximum allowed length is '
                f'{EMAIL_MAX_LENGTH} characters',
            )

        if self.email and re.match(EMAIL_PATTERN, self.email) is None:
            raise UserValidationError('email has an invalid format')
