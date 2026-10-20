from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final, override

from django.db import IntegrityError
from django.db.models import F as Field

from server.apps.shortify.application.exceptions import ShortLinkCollisionError
from server.apps.shortify.application.interfaces.repositories import (
    ShortLinkRepositoryProtocol,
)
from server.apps.shortify.domain.entities import ShortLinkEntity
from server.apps.shortify.infrastructure.models import ShortLink

if TYPE_CHECKING:
    from server.apps.shortify.infrastructure.mappers import ShortLinkDBMapper
    from server.common.transaction import TransactionProtocol


@final
@dataclass(frozen=True, slots=True)
class ShortLinkRepository(ShortLinkRepositoryProtocol):
    _mapper: ShortLinkDBMapper
    _transaction: TransactionProtocol

    @override
    def create(self, *, original_url: str, short_code: str) -> ShortLinkEntity:
        try:
            with self._transaction():
                short_link_instance = ShortLink.objects.create(
                    original_url=original_url, short_code=short_code
                )
        except IntegrityError as exc:
            raise ShortLinkCollisionError(short_code) from exc
        return self._mapper.single(link=short_link_instance)

    @override
    def get_by_code(self, *, short_code: str) -> ShortLinkEntity | None:
        try:
            short_link_instance = ShortLink.objects.get(short_code=short_code)
        except ShortLink.DoesNotExist:
            return None
        return self._mapper.single(link=short_link_instance)

    @override
    def increment_clicks(self, *, short_code: str) -> None:
        ShortLink.objects.filter(short_code=short_code).update(
            clicks=Field('clicks') + 1,
        )
