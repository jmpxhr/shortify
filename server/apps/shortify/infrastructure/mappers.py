from collections.abc import Iterable
from dataclasses import dataclass
from typing import final

from server.apps.shortify.domain.entities import ClickEventEntity, ShortLinkEntity
from server.apps.shortify.infrastructure.models import ClickEvent, ShortLink


@final
@dataclass(frozen=True, slots=True)
class ShortLinkDBMapper:
    """Map a ``Task`` Django model to its Entity"""

    def single(self, *, link: ShortLink) -> ShortLinkEntity:
        return ShortLinkEntity(
            id=link.pk,
            original_url=link.original_url,
            short_code=link.short_code,
            created_at=link.created_at,
            clicks=link.clicks,
            owner_id=link.owner_id,
        )

    def many(self, *, links: Iterable[ShortLink]) -> list[ShortLinkEntity]:
        return [self.single(link=link) for link in links]


@final
@dataclass(frozen=True, slots=True)
class ClickEventDBMapper:
    """Map a ``ClickEvent`` Django model to its Entity."""

    def single(self, *, event: ClickEvent) -> ClickEventEntity:
        return ClickEventEntity(
            id=event.pk,
            short_link_id=event.short_link_id,
            clicked_at=event.clicked_at,
            country_code=event.country_code,
            region=event.region,
            city=event.city,
            referrer_host=event.referrer_host,
            device_type=event.device_type,
            browser=event.browser,
            os=event.os,
        )

    def many(self, *, events: Iterable[ClickEvent]) -> list[ClickEventEntity]:
        return [self.single(event=event) for event in events]
