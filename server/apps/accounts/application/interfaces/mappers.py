from abc import abstractmethod
from typing import Protocol

from server.apps.accounts.application.dtos.user import UserDTO
from server.apps.accounts.domain.entities import UserEntity


class EntityDtoUserMapperProtocol(Protocol):
    @abstractmethod
    def to_dto(self, entity: UserEntity) -> UserDTO: ...
