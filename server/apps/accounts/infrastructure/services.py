from dataclasses import dataclass
from typing import final, override

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from server.apps.accounts.application.exceptions import WeakPasswordError
from server.apps.accounts.application.interfaces.services import (
    PasswordValidatorProtocol,
)


@final
@dataclass(frozen=True, slots=True)
class DjangoPasswordValidator(PasswordValidatorProtocol):
    @override
    def validate_password(
        self,
        *,
        password: str,
        username: str,
        email: str,
    ) -> None:
        user = User(username=username, email=email)
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise WeakPasswordError(exc.messages) from exc
