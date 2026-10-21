from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.accounts.application.dtos.user import UserDTO
from server.apps.accounts.application.exceptions import UserNotFoundError

if TYPE_CHECKING:
    from server.apps.accounts.application.interfaces.mappers import (
        EntityDtoUserMapperProtocol,
    )
    from server.apps.accounts.application.interfaces.repositories import (
        UserRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class GetCurrentUser:
    _repository: UserRepositoryProtocol
    _mapper: EntityDtoUserMapperProtocol

    def __call__(self, *, user_id: int) -> UserDTO:
        entity = self._repository.get_by_id(user_id=user_id)
        if entity is None:
            raise UserNotFoundError(user_id=user_id)
        return self._mapper.to_dto(entity)
