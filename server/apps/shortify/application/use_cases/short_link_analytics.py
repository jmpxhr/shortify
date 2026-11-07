from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType
from typing import TYPE_CHECKING, Final, final

from django.utils import timezone

from server.apps.shortify.application.dtos.analytics import (
    AnalyticsBucketDTO,
    AnalyticsRange,
    LinkAnalyticsDTO,
)
from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.repositories import (
        ClickEventDimension,
        ClickEventRepositoryProtocol,
        ShortLinkRepositoryProtocol,
    )

_UNKNOWN = 'unknown'
_DIRECT = 'direct'

_RANGE_DAYS: Final = MappingProxyType({
    '7d': 7,
    '30d': 30,
    '90d': 90,
})


@final
@dataclass(frozen=True, slots=True)
class GetLinkAnalytics:
    _repository: ShortLinkRepositoryProtocol
    _event_repository: ClickEventRepositoryProtocol

    def __call__(
        self,
        *,
        short_code: str,
        owner_id: int,
        time_range: AnalyticsRange = '30d',
    ) -> LinkAnalyticsDTO:
        short_link_entity = self._repository.get_by_code_and_owner(
            short_code=short_code,
            owner_id=owner_id,
        )
        if short_link_entity is None:
            raise ShortLinkNotFoundError(short_code=short_code)

        since = self._since(time_range)
        return LinkAnalyticsDTO(
            total_clicks=short_link_entity.clicks,
            range_clicks=self._event_repository.count_in_range(
                short_link_id=short_link_entity.id,
                since=since,
            ),
            range=time_range,
            countries=self._buckets(
                short_link_id=short_link_entity.id,
                dimension='country_code',
                since=since,
                fallback=_UNKNOWN,
            ),
            referrers=self._buckets(
                short_link_id=short_link_entity.id,
                dimension='referrer_host',
                since=since,
                fallback=_DIRECT,
            ),
            devices=self._buckets(
                short_link_id=short_link_entity.id,
                dimension='device_type',
                since=since,
                fallback=_UNKNOWN,
            ),
            browsers=self._buckets(
                short_link_id=short_link_entity.id,
                dimension='browser',
                since=since,
                fallback=_UNKNOWN,
            ),
            operating_systems=self._buckets(
                short_link_id=short_link_entity.id,
                dimension='os',
                since=since,
                fallback=_UNKNOWN,
            ),
        )

    def _since(self, time_range: AnalyticsRange) -> datetime | None:
        days = _RANGE_DAYS.get(time_range)
        if days is None:
            return None
        return timezone.now() - timedelta(days=days)

    def _buckets(
        self,
        *,
        short_link_id: int,
        dimension: ClickEventDimension,
        since: datetime | None,
        fallback: str,
    ) -> list[AnalyticsBucketDTO]:
        buckets = [
            AnalyticsBucketDTO(value=bucket_value or fallback, count=count)
            for bucket_value, count in self._event_repository.breakdown(
                short_link_id=short_link_id,
                dimension=dimension,
                since=since,
            )
        ]
        buckets.sort(key=lambda bucket: (-bucket.count, bucket.value))
        return buckets
