from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.accounts.application.dtos.user import UserDTO
from server.apps.accounts.application.exceptions import UserNotFoundError
from server.apps.accounts.domain.entities import UserEntity

if TYPE_CHECKING:
    from server.apps.accounts.application.interfaces.mappers import (
        EntityDtoUserMapperProtocol,
    )
    from server.apps.accounts.application.interfaces.repositories import (
        UserRepositoryProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class UpdateCurrentUser:
    _repository: UserRepositoryProtocol
    _mapper: EntityDtoUserMapperProtocol

    def __call__(
        self,
        *,
        user_id: int,
        username: str | None,
        email: str | None,
    ) -> UserDTO:
        existing = self._repository.get_by_id(user_id=user_id)
        if existing is None:
            raise UserNotFoundError(user_id=user_id)

        # Reuse domain validation from ``UserEntity.__post_init__``.
        updated_entity = UserEntity(
            id=existing.id,
            username=existing.username if username is None else username,
            email=existing.email if email is None else email,
        )
        persisted = self._repository.update_user(
            user_id=updated_entity.id,
            username=updated_entity.username,
            email=updated_entity.email,
        )
        return self._mapper.to_dto(persisted)
