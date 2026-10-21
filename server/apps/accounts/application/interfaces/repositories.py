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

    @abstractmethod
    def get_by_id(self, *, user_id: int) -> UserEntity | None: ...

    @abstractmethod
    def update_user(
        self,
        *,
        user_id: int,
        username: str,
        email: str,
    ) -> UserEntity: ...

    @abstractmethod
    def delete_user(self, *, user_id: int) -> None: ...
