from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.accounts.application.dtos.user import UserDTO

if TYPE_CHECKING:
    from server.apps.accounts.application.interfaces.mappers import (
        EntityDtoUserMapperProtocol,
    )
    from server.apps.accounts.application.interfaces.repositories import (
        UserRepositoryProtocol,
    )
    from server.apps.accounts.application.interfaces.services import (
        PasswordValidatorProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class RegisterUser:
    _password_validator: PasswordValidatorProtocol
    _repository: UserRepositoryProtocol
    _mapper: EntityDtoUserMapperProtocol

    def __call__(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> UserDTO:
        self._password_validator.validate_password(
            password=password,
            username=username,
            email=email,
        )
        user_entity = self._repository.create_user(
            username=username,
            email=email,
            password=password,
        )
        return self._mapper.to_dto(user_entity)
