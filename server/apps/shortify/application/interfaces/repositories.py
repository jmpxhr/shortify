from abc import abstractmethod
from typing import Protocol

from server.apps.shortify.domain.entities import ShortLinkEntity


class ShortLinkRepositoryProtocol(Protocol):
    @abstractmethod
    def create(
        self,
        *,
        original_url: str,
        short_code: str,
        owner_id: int,
    ) -> ShortLinkEntity: ...

    @abstractmethod
    def get_by_code(self, *, short_code: str) -> ShortLinkEntity | None: ...

    @abstractmethod
    def list_by_owner(
        self,
        *,
        owner_id: int,
        limit: int,
        offset: int,
    ) -> tuple[list[ShortLinkEntity], int]: ...

    @abstractmethod
    def get_by_code_and_owner(
        self,
        *,
        short_code: str,
        owner_id: int,
    ) -> ShortLinkEntity | None: ...

    @abstractmethod
    def delete_by_code_and_owner(
        self,
        *,
        short_code: str,
        owner_id: int,
    ) -> bool: ...

    @abstractmethod
    def increment_clicks(self, *, short_code: str) -> None: ...
