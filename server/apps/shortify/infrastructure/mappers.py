from collections.abc import Iterable
from dataclasses import dataclass
from typing import final

from server.apps.shortify.domain.entities import ShortLinkEntity
from server.apps.shortify.models import ShortLink


@final
@dataclass(frozen=True, slots=True)
class ShortLinkMapper:
    """Map a ``Task`` Django model to its Entity"""

    def single(self, *, link: ShortLink) -> ShortLinkEntity:
        return ShortLinkEntity(
            original_url=link.original_url,
            short_code=link.short_code,
            create_at=link.created_at,
            updated_at=link.updated_at,
        )

    def many(self, *, links: Iterable[ShortLink]) -> list[ShortLinkEntity]:
        return [self.single(link=link) for link in links]
