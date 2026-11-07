from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ClickContextDTO:
    """Request data used to derive click-event attributes."""

    ip_address: str | None = None
    user_agent: str | None = None
    referrer: str | None = None


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class GeolocationDTO:
    """Location attributes derived from an IP address."""

    country_code: str | None = None
    region: str | None = None
    city: str | None = None


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ClickAgentDTO:
    """Device attributes derived from a User-Agent header."""

    device_type: str | None = None
    browser: str | None = None
    os: str | None = None
