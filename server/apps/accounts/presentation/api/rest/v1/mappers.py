from dataclasses import dataclass
from typing import final

from server.apps.accounts.application.dtos.user import UserDTO
from server.apps.accounts.presentation.api.rest.v1.schemas import (
    UserResponseSchema,
)


@final
@dataclass(frozen=True, slots=True)
class UserPresentationMapper:
    def __call__(self, *, user: UserDTO) -> UserResponseSchema:
        return UserResponseSchema(
            id=user.id,
            username=user.username,
            email=user.email,
        )
