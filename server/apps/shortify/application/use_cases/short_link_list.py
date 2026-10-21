from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.dtos.short_link import ShortLinkPageDTO

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.mappers import (
        EntityDtoShortLinkMapperProtocol,
    )
    from server.apps.shortify.application.interfaces.repositories import (
        ShortLinkRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class ListShortLinks:
    _mapper: EntityDtoShortLinkMapperProtocol
    _repository: ShortLinkRepositoryProtocol

    def __call__(
        self,
        *,
        owner_id: int,
        page: int,
        page_size: int,
    ) -> ShortLinkPageDTO:
        offset = (page - 1) * page_size
        short_link_entities, total = self._repository.list_by_owner(
            owner_id=owner_id,
            limit=page_size,
            offset=offset,
        )
        return ShortLinkPageDTO(
            total=total,
            short_links=[
                self._mapper.to_dto(short_link_entity)
                for short_link_entity in short_link_entities
            ],
        )
