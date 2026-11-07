from typing import Annotated, final

import msgspec

from server.apps.shortify.application.dtos.analytics import AnalyticsRange


@final
class ShortLinkAnalyticsQuery(msgspec.Struct):
    """Time range for a link's analytics report."""

    range: Annotated[
        AnalyticsRange,
        msgspec.Meta(examples=['30d']),
    ] = '30d'


@final
class AnalyticsBucketSchema(msgspec.Struct):
    """One counted value in an analytics breakdown."""

    value: Annotated[str, msgspec.Meta(examples=['DE'])]  # noqa: WPS110
    count: Annotated[int, msgspec.Meta(ge=0, examples=[40])]


@final
class ShortLinkAnalyticsSchema(msgspec.Struct):
    """Aggregated analytics for a single short link."""

    total_clicks: Annotated[int, msgspec.Meta(ge=0, examples=[142])]
    range_clicks: Annotated[int, msgspec.Meta(ge=0, examples=[87])]
    range: Annotated[str, msgspec.Meta(examples=['30d'])]
    countries: list[AnalyticsBucketSchema]
    referrers: list[AnalyticsBucketSchema]
    devices: list[AnalyticsBucketSchema]
    browsers: list[AnalyticsBucketSchema]
    operating_systems: list[AnalyticsBucketSchema]
