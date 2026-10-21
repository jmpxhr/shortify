from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.repositories import (
        ShortLinkRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class DeleteShortLink:
    _repository: ShortLinkRepositoryProtocol

    def __call__(self, *, short_code: str, owner_id: int) -> None:
        deleted = self._repository.delete_by_code_and_owner(
            short_code=short_code,
            owner_id=owner_id,
        )
        if not deleted:
            raise ShortLinkNotFoundError(short_code=short_code)
