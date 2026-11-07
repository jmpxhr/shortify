from abc import abstractmethod
from datetime import datetime
from typing import Literal, Protocol

from server.apps.shortify.domain.entities import ClickEventEntity, ShortLinkEntity

ClickEventDimension = Literal[
    'country_code',
    'referrer_host',
    'device_type',
    'browser',
    'os',
]


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


class ClickEventRepositoryProtocol(Protocol):
    @abstractmethod
    def create(  # noqa: WPS211
        self,
        *,
        short_link_id: int,
        country_code: str | None,
        region: str | None,
        city: str | None,
        referrer_host: str | None,
        device_type: str | None,
        browser: str | None,
        os: str | None,
    ) -> ClickEventEntity: ...

    @abstractmethod
    def count_in_range(
        self,
        *,
        short_link_id: int,
        since: datetime | None,
    ) -> int: ...

    @abstractmethod
    def breakdown(
        self,
        *,
        short_link_id: int,
        dimension: ClickEventDimension,
        since: datetime | None,
    ) -> list[tuple[str | None, int]]: ...
