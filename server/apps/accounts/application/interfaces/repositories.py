from abc import abstractmethod
from typing import Protocol

from server.apps.accounts.domain.entities import UserEntity


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> UserEntity: ...
