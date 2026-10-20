from dataclasses import dataclass
from typing import final, override

from server.apps.accounts.application.dtos.user import UserDTO
from server.apps.accounts.application.interfaces.mappers import (
    EntityDtoUserMapperProtocol,
)
from server.apps.accounts.domain.entities import UserEntity


@final
@dataclass(frozen=True, slots=True)
class UserMapper(EntityDtoUserMapperProtocol):
    @override
    def to_dto(self, entity: UserEntity) -> UserDTO:
        return UserDTO(
            id=entity.id,
            username=entity.username,
            email=entity.email,
        )
