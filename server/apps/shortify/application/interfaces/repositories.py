from abc import abstractmethod
from typing import Protocol

from server.apps.shortify.domain.entities import ShortLinkEntity


class ShortLinkRepositoryProtocol(Protocol):
    @abstractmethod
    def create(self, *, original_url: str, short_code: str) -> ShortLinkEntity: ...

    @abstractmethod
    def get_by_code(self, *, short_code: str) -> ShortLinkEntity | None: ...

    @abstractmethod
    def increment_clicks(self, *, short_code: str) -> None: ...
