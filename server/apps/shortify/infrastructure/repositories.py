from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, final, override

from django.db import IntegrityError
from django.db.models import Count, QuerySet
from django.db.models import F as Field

from server.apps.shortify.application.exceptions import ShortLinkCollisionError
from server.apps.shortify.application.interfaces.repositories import (
    ClickEventDimension,
    ClickEventRepositoryProtocol,
    ShortLinkRepositoryProtocol,
)
from server.apps.shortify.domain.entities import ClickEventEntity, ShortLinkEntity
from server.apps.shortify.infrastructure.models import ClickEvent, ShortLink

if TYPE_CHECKING:
    from server.apps.shortify.infrastructure.mappers import (
        ClickEventDBMapper,
        ShortLinkDBMapper,
    )
    from server.common.transaction import TransactionProtocol


@final
@dataclass(frozen=True, slots=True)
class ShortLinkRepository(ShortLinkRepositoryProtocol):
    _mapper: ShortLinkDBMapper
    _transaction: TransactionProtocol

    @override
    def create(
        self,
        *,
        original_url: str,
        short_code: str,
        owner_id: int,
    ) -> ShortLinkEntity:
        try:
            with self._transaction():
                short_link_instance = ShortLink.objects.create(
                    original_url=original_url,
                    short_code=short_code,
                    owner_id=owner_id,
                )
        except IntegrityError as exc:
            raise ShortLinkCollisionError(short_code) from exc
        return self._mapper.single(link=short_link_instance)

    @override
    def get_by_code(self, *, short_code: str) -> ShortLinkEntity | None:
        try:
            short_link_instance = ShortLink.objects.get(short_code=short_code)
        except ShortLink.DoesNotExist:
            return None
        return self._mapper.single(link=short_link_instance)

    @override
    def list_by_owner(
        self,
        *,
        owner_id: int,
        limit: int,
        offset: int,
    ) -> tuple[list[ShortLinkEntity], int]:
        queryset = ShortLink.objects.filter(owner_id=owner_id)
        total = queryset.count()
        short_link_instances = queryset.order_by('-created_at', '-pk')[
            offset : offset + limit
        ]
        return self._mapper.many(links=short_link_instances), total

    @override
    def get_by_code_and_owner(
        self,
        *,
        short_code: str,
        owner_id: int,
    ) -> ShortLinkEntity | None:
        short_link_instance = ShortLink.objects.filter(
            short_code=short_code,
            owner_id=owner_id,
        ).first()
        if short_link_instance is None:
            return None
        return self._mapper.single(link=short_link_instance)

    @override
    def delete_by_code_and_owner(
        self,
        *,
        short_code: str,
        owner_id: int,
    ) -> bool:
        deleted_count, _ = ShortLink.objects.filter(
            short_code=short_code,
            owner_id=owner_id,
        ).delete()
        return bool(deleted_count)

    @override
    def increment_clicks(self, *, short_code: str) -> None:
        ShortLink.objects.filter(short_code=short_code).update(
            clicks=Field('clicks') + 1,
        )


@final
@dataclass(frozen=True, slots=True)
class ClickEventRepository(ClickEventRepositoryProtocol):
    _mapper: ClickEventDBMapper

    @override
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
    ) -> ClickEventEntity:
        event_instance = ClickEvent.objects.create(
            short_link_id=short_link_id,
            country_code=country_code,
            region=region,
            city=city,
            referrer_host=referrer_host,
            device_type=device_type,
            browser=browser,
            os=os,
        )
        return self._mapper.single(event=event_instance)

    @override
    def count_in_range(
        self,
        *,
        short_link_id: int,
        since: datetime | None,
    ) -> int:
        return self._in_range(
            short_link_id=short_link_id,
            since=since,
        ).count()

    @override
    def breakdown(
        self,
        *,
        short_link_id: int,
        dimension: ClickEventDimension,
        since: datetime | None,
    ) -> list[tuple[str | None, int]]:
        rows = (
            self
            ._in_range(short_link_id=short_link_id, since=since)
            .values(dimension)
            .annotate(count=Count('id'))
            .order_by('-count', dimension)
        )
        return [(row[dimension], row['count']) for row in rows]

    def _in_range(
        self,
        *,
        short_link_id: int,
        since: datetime | None,
    ) -> QuerySet[ClickEvent]:
        queryset = ClickEvent.objects.filter(short_link_id=short_link_id)
        if since is not None:
            queryset = queryset.filter(clicked_at__gte=since)
        return queryset
