from dataclasses import dataclass
from typing import final

from server.apps.shortify.application.dtos.short_link import ShortLinkDTO
from server.apps.shortify.presentation.api.rest.v1.schemas import (
    ShortLinkResponseSchema,
)


@final
@dataclass(frozen=True, slots=True)
class ShortLinkPresentationMapper:
    def __call__(self, *, short_link: ShortLinkDTO) -> ShortLinkResponseSchema:
        return ShortLinkResponseSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
        )
