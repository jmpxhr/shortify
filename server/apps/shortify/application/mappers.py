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
    def to_entity(self, dto: ShortLinkDTO) -> ShortLinkEntity:
        return ShortLinkEntity(
            original_url=dto.original_url,
            short_code=dto.short_code,
            create_at=dto.create_at,
            updated_at=dto.updated_at,
        )

    @override
    def to_dto(self, entitiy: ShortLinkEntity) -> ShortLinkDTO:
        return ShortLinkDTO(
            original_url=entitiy.original_url,
            short_code=entitiy.short_code,
            create_at=entitiy.create_at,
            updated_at=entitiy.updated_at,
        )
