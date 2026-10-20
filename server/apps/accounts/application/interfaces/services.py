from abc import abstractmethod
from typing import Protocol


class PasswordValidatorProtocol(Protocol):
    @abstractmethod
    def validate_password(
        self,
        *,
        password: str,
        username: str,
        email: str,
    ) -> None: ...
