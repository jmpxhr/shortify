from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final, override

from django.contrib.auth.models import User
from django.db import IntegrityError

from server.apps.accounts.application.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
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

    @override
    def get_by_id(self, *, user_id: int) -> UserEntity | None:
        user_instance = User.objects.filter(pk=user_id).first()
        if user_instance is None:
            return None
        return self._mapper.single(user=user_instance)

    @override
    def update_user(
        self,
        *,
        user_id: int,
        username: str,
        email: str,
    ) -> UserEntity:
        try:
            user_instance = User.objects.get(pk=user_id)
        except User.DoesNotExist as exc:
            raise UserNotFoundError(user_id=user_id) from exc

        user_instance.username = username
        user_instance.email = email
        try:
            user_instance.save(update_fields=('username', 'email'))
        except IntegrityError as exc:
            raise UserAlreadyExistsError(username=username) from exc
        return self._mapper.single(user=user_instance)

    @override
    def delete_user(self, *, user_id: int) -> None:
        User.objects.filter(pk=user_id).delete()
