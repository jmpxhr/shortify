import math
from dataclasses import dataclass
from typing import final

from dmr.pagination import Page, Paginated

from server.apps.shortify.application.dtos.analytics import (
    AnalyticsBucketDTO,
    LinkAnalyticsDTO,
)
from server.apps.shortify.application.dtos.short_link import (
    ShortLinkDTO,
    ShortLinkPageDTO,
)
from server.apps.shortify.presentation.api.rest.v1.analytics_schemas import (
    AnalyticsBucketSchema,
    ShortLinkAnalyticsSchema,
)
from server.apps.shortify.presentation.api.rest.v1.schemas import (
    ShortLinkDetailSchema,
    ShortLinkResponseSchema,
)


@final
@dataclass(frozen=True, slots=True)
class ShortLinkPresentationMapper:
    def __call__(self, *, short_link: ShortLinkDTO) -> ShortLinkResponseSchema:
        return ShortLinkResponseSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
            clicks=short_link.clicks,
        )

    def detail(self, *, short_link: ShortLinkDTO) -> ShortLinkDetailSchema:
        return ShortLinkDetailSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
            clicks=short_link.clicks,
            created_at=short_link.created_at,
        )

    def page(
        self,
        *,
        page: ShortLinkPageDTO,
        number: int,
        per_page: int,
    ) -> Paginated[ShortLinkResponseSchema]:
        return Paginated(
            count=page.total,
            num_pages=max(1, math.ceil(page.total / per_page)),
            per_page=per_page,
            page=Page(
                number=number,
                object_list=[
                    self(short_link=short_link) for short_link in page.short_links
                ],
            ),
        )

    def analytics(self, *, analytics: LinkAnalyticsDTO) -> ShortLinkAnalyticsSchema:
        return ShortLinkAnalyticsSchema(
            total_clicks=analytics.total_clicks,
            range_clicks=analytics.range_clicks,
            range=analytics.range,
            countries=self._buckets(analytics.countries),
            referrers=self._buckets(analytics.referrers),
            devices=self._buckets(analytics.devices),
            browsers=self._buckets(analytics.browsers),
            operating_systems=self._buckets(analytics.operating_systems),
        )

    def _buckets(
        self,
        buckets: list[AnalyticsBucketDTO],
    ) -> list[AnalyticsBucketSchema]:
        return [
            AnalyticsBucketSchema(value=bucket.value, count=bucket.count)
            for bucket in buckets
        ]
