from dataclasses import dataclass
from typing import final

from django.contrib.auth.models import User

from server.apps.accounts.domain.entities import UserEntity


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper:
    """Map a Django ``User`` model to its entity."""

    def single(self, *, user: User) -> UserEntity:
        return UserEntity(
            id=user.pk,
            username=user.username,
            email=user.email,
        )
