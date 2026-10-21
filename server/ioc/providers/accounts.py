from collections.abc import Callable
from typing import Any

import punq


def inject_accounts(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from server.apps.accounts.application.interfaces.mappers import (
        EntityDtoUserMapperProtocol,
    )
    from server.apps.accounts.application.interfaces.repositories import (
        UserRepositoryProtocol,
    )
    from server.apps.accounts.application.interfaces.services import (
        PasswordValidatorProtocol,
    )
    from server.apps.accounts.application.mappers import UserMapper
    from server.apps.accounts.application.use_cases import (
        DeleteCurrentUser,
        GetCurrentUser,
        RegisterUser,
        UpdateCurrentUser,
    )
    from server.apps.accounts.infrastructure.mappers import UserDBMapper
    from server.apps.accounts.infrastructure.repositories import DjangoUserRepository
    from server.apps.accounts.infrastructure.services import DjangoPasswordValidator
    from server.apps.accounts.presentation.api.rest.v1.mappers import (
        UserPresentationMapper,
    )

    container.register(UserPresentationMapper)
    container.register(EntityDtoUserMapperProtocol, UserMapper)
    container.register(UserDBMapper)
    container.register(UserRepositoryProtocol, DjangoUserRepository)
    container.register(PasswordValidatorProtocol, DjangoPasswordValidator)
    container.register(inject(RegisterUser))
    container.register(inject(GetCurrentUser))
    container.register(inject(UpdateCurrentUser))
    container.register(inject(DeleteCurrentUser))
