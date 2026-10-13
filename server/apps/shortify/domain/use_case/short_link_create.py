from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.domain.constants import SHORT_CODE_LENGTH

if TYPE_CHECKING:
    from server.apps.shortify.domain import services
    from server.apps.shortify.domain.entities import ShortLinkEntity
    from server.apps.shortify.infrastructure import mappers, repositories


# TODO: retries for collision
@final
@dataclass(frozen=True, slots=True)
class CreateShortLink:
    _repository: repositories.ShortLinkRepository
    _mapper: mappers.ShortLinkMapper
    _service: services.ShortLinkGeneratorService

    def __call__(self, *, original_url: str) -> ShortLinkEntity:
        return self._mapper.single(
            link=self._repository.create(
                original_url=original_url,
                short_code=self._service.generate_code(
                    length=SHORT_CODE_LENGTH,
                ),
            )
        )
