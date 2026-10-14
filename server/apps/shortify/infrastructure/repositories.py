from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final, override

from django.db import IntegrityError

from server.apps.shortify.application.exceptions import ShortLinkCollisionError
from server.apps.shortify.application.interfaces.repositories import (
    ShortLinkRepositoryProtocol,
)
from server.apps.shortify.domain.entities import ShortLinkEntity
from server.apps.shortify.infrastructure.models import ShortLink

if TYPE_CHECKING:
    from server.apps.shortify.infrastructure.mappers import ShortLinkDBMapper


@final
@dataclass(frozen=True, slots=True)
class ShortLinkRepository(ShortLinkRepositoryProtocol):
    _mapper: ShortLinkDBMapper

    @override
    def create(self, *, original_url: str, short_code: str) -> ShortLinkEntity:
        try:
            short_link_instance = ShortLink.objects.create(
                original_url=original_url, short_code=short_code
            )
            return self._mapper.single(link=short_link_instance)
        except IntegrityError as exc:
            raise ShortLinkCollisionError(short_code) from exc

    @override
    def get_by_code(self, *, short_code: str) -> ShortLinkEntity | None:
        try:
            short_link_instance = ShortLink.objects.get(short_code=short_code)
            return self._mapper.single(link=short_link_instance)
        except ShortLink.DoesNotExist:
            return None
