from dataclasses import dataclass
from datetime import datetime
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkDTO:
    original_url: str
    short_code: str
    create_at: datetime
    updated_at: datetime
