from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.accounts.application.exceptions import UserNotFoundError

if TYPE_CHECKING:
    from server.apps.accounts.application.interfaces.repositories import (
        UserRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class DeleteCurrentUser:
    _repository: UserRepositoryProtocol

    def __call__(self, *, user_id: int) -> None:
        if self._repository.get_by_id(user_id=user_id) is None:
            raise UserNotFoundError(user_id=user_id)
        self._repository.delete_user(user_id=user_id)
