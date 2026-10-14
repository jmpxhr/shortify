from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.dtos.short_link import ShortLinkDTO
from server.apps.shortify.domain.constants import SHORT_CODE_LENGTH

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces import (
        mappers,
        repositories,
        services,
    )


# TODO: retries for collision
@final
@dataclass(frozen=True, slots=True)
class CreateShortLink:
    _mapper: mappers.EntityDtoShortLinkMapperProtocol
    _repository: repositories.ShortLinkRepositoryProtocol
    _service: services.ShortLinkGeneratorServiceProtocol

    def __call__(self, *, original_url: str) -> ShortLinkDTO:
        short_code = self._service.generate_code(length=SHORT_CODE_LENGTH)
        short_link_entity = self._repository.create(
            original_url=original_url, short_code=short_code
        )
        return self._mapper.to_dto(short_link_entity)
