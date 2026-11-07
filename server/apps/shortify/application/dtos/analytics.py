from dataclasses import dataclass
from typing import Literal, final

AnalyticsRange = Literal['7d', '30d', '90d', 'all']


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class AnalyticsBucketDTO:
    value: str  # noqa: WPS110
    count: int


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class LinkAnalyticsDTO:
    total_clicks: int
    range_clicks: int
    range: str
    countries: list[AnalyticsBucketDTO]
    referrers: list[AnalyticsBucketDTO]
    devices: list[AnalyticsBucketDTO]
    browsers: list[AnalyticsBucketDTO]
    operating_systems: list[AnalyticsBucketDTO]
