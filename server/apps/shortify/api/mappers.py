from dataclasses import dataclass
from typing import final

from server.apps.shortify.api.schemas import ShortLinkResponseSchema
from server.apps.shortify.domain.entities import ShortLinkEntity


@final
@dataclass(frozen=True, slots=True)
class ShortLinkDtoMapper:
    def __call__(self, *, short_link: ShortLinkEntity) -> ShortLinkResponseSchema:
        return ShortLinkResponseSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
        )
