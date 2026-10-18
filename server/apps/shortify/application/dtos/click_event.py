from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ClickContext:
    referer: str = ''
    user_agent: str = ''
    ip: str | None = None
