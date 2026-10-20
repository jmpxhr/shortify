from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.repositories import (
        ShortLinkRepositoryProtocol,
    )
    from server.common.transaction import TransactionProtocol


@final
@dataclass(frozen=True, slots=True)
class GetUrlFromShortLink:
    _repository: ShortLinkRepositoryProtocol
    _transaction: TransactionProtocol

    def __call__(self, *, short_code: str) -> str:
        with self._transaction():
            short_link_entity = self._repository.get_by_code(short_code=short_code)
            if short_link_entity is None:
                raise ShortLinkNotFoundError(short_code=short_code)
            self._repository.increment_clicks(short_code=short_code)
            return short_link_entity.original_url
