from dataclasses import dataclass
from typing import final, override

from server.apps.shortify.application.dtos.short_link import ShortLinkDTO
from server.apps.shortify.application.interfaces.mappers import (
    EntityDtoShortLinkMapperProtocol,
)
from server.apps.shortify.domain.entities import ShortLinkEntity


@final
@dataclass(frozen=True, slots=True)
class ShortLinkMapper(EntityDtoShortLinkMapperProtocol):
    @override
    def to_dto(self, entity: ShortLinkEntity) -> ShortLinkDTO:
        return ShortLinkDTO(
            original_url=entity.original_url,
            short_code=entity.short_code,
            created_at=entity.created_at,
            clicks=entity.clicks,
            owner_id=entity.owner_id,
        )
