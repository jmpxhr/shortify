from collections.abc import Iterable
from dataclasses import dataclass
from typing import final

from server.apps.shortify.domain.entities import ShortLinkEntity
from server.apps.shortify.infrastructure.models import ShortLink


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
            owner_id=link.owner_id,  # pyrefly: ignore [missing-attribute]
        )

    def many(self, *, links: Iterable[ShortLink]) -> list[ShortLinkEntity]:
        return [self.single(link=link) for link in links]
