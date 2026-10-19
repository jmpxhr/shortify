# NOTE: simple layers go on top!

from collections.abc import Callable
from typing import Any

import punq


def _global_namespace() -> dict[str, Any]:
    from django.conf import LazySettings
    from django.core.cache import BaseCache

    return locals()  # noqa: WPS421


def _create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    # We need to provide the same string names as we do in the definition.
    localns.pop('container')
    localns.update(_global_namespace())
    # pyrefly: ignore [missing-attribute]
    # ruff: ignore[private-member-access]
    container.registrations._localns.update(localns)
    return lambda service: service


def _inject_django(container: punq.Container) -> None:
    from django.conf import LazySettings, settings

    # Django:
    container.register(
        LazySettings,
        instance=settings,
        scope=punq.Scope.singleton,
    )


def _inject_mappers(container: punq.Container) -> None:
    from server.apps.shortify.application.interfaces.mappers import (
        EntityDtoShortLinkMapperProtocol,
    )
    from server.apps.shortify.application.mappers import ShortLinkMapper
    from server.apps.shortify.infrastructure.mappers import ShortLinkDBMapper
    from server.apps.shortify.presentation.api.rest.v1.mappers import (
        ShortLinkPresentationMapper,
    )

    container.register(ShortLinkPresentationMapper)
    container.register(EntityDtoShortLinkMapperProtocol, ShortLinkMapper)
    container.register(ShortLinkDBMapper)


def _inject_repositories(container: punq.Container) -> None:
    from server.apps.shortify.application.interfaces.repositories import (
        ShortLinkRepositoryProtocol,
    )
    from server.apps.shortify.infrastructure.repositories import ShortLinkRepository

    container.register(ShortLinkRepositoryProtocol, ShortLinkRepository)


def _inject_services(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from server.apps.shortify.application.interfaces.services import (
        EncoderProtocol,
        ShortLinkGeneratorServiceProtocol,
    )
    from server.apps.shortify.domain.constants import ENCODING_ALPHABET
    from server.apps.shortify.infrastructure.services import (
        Base62EncoderService,
        ShortLinkGeneratorService,
    )

    container.register(EncoderProtocol, Base62EncoderService)
    container.register(
        ShortLinkGeneratorServiceProtocol,
        inject(ShortLinkGeneratorService),
        _alphabet=ENCODING_ALPHABET,
    )


def _inject_use_cases(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from server.apps.shortify.application import use_cases

    container.register(inject(use_cases.CreateShortLink))
    container.register(inject(use_cases.GetUrlFromShortLink))


def _inject_shortify(container: punq.Container) -> None:
    from server.apps.shortify.application.interfaces.transactions import (
        TransactionProtocol,
    )
    from server.apps.shortify.infrastructure.transactions import TransactionAtomic

    # Hacks to resolve annotations:
    inject = _create_injector(container, locals())  # noqa: WPS421

    container.register(TransactionProtocol, TransactionAtomic)

    _inject_mappers(container)
    _inject_repositories(container)
    _inject_services(container, inject=inject)
    _inject_use_cases(container, inject=inject)


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populates dependencies for the container."""
    # Deps:
    _inject_django(container)
    # Apps:
    _inject_shortify(container)
    return container
