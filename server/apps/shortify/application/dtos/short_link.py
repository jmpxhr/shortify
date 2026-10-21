from dataclasses import dataclass
from datetime import datetime
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkDTO:
    original_url: str
    short_code: str
    created_at: datetime
    clicks: int
    owner_id: int | None = None


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkPageDTO:
    total: int
    short_links: list[ShortLinkDTO]
