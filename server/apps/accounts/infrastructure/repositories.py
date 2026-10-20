from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final, override

from django.contrib.auth.models import User
from django.db import IntegrityError

from server.apps.accounts.application.exceptions import UserAlreadyExistsError
from server.apps.accounts.application.interfaces.repositories import (
    UserRepositoryProtocol,
)
from server.apps.accounts.domain.entities import UserEntity

if TYPE_CHECKING:
    from server.apps.accounts.infrastructure.mappers import UserDBMapper


@final
@dataclass(frozen=True, slots=True)
class DjangoUserRepository(UserRepositoryProtocol):
    _mapper: UserDBMapper

    @override
    def create_user(
        self,
        *,
        username: str,
        email: str,
        password: str,
    ) -> UserEntity:
        try:
            user_instance = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
        except IntegrityError as exc:
            raise UserAlreadyExistsError(username=username) from exc
        return self._mapper.single(user=user_instance)
