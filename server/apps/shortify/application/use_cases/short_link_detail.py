from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.dtos.short_link import ShortLinkDTO
from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.mappers import (
        EntityDtoShortLinkMapperProtocol,
    )
    from server.apps.shortify.application.interfaces.repositories import (
        ShortLinkRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class GetShortLink:
    _mapper: EntityDtoShortLinkMapperProtocol
    _repository: ShortLinkRepositoryProtocol

    def __call__(self, *, short_code: str, owner_id: int) -> ShortLinkDTO:
        short_link_entity = self._repository.get_by_code_and_owner(
            short_code=short_code,
            owner_id=owner_id,
        )
        if short_link_entity is None:
            raise ShortLinkNotFoundError(short_code=short_code)
        return self._mapper.to_dto(short_link_entity)
