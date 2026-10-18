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


# TODO: Resolve WPS213
def _inject_shortify(container: punq.Container) -> None:  # noqa: WPS213
    from server.apps.shortify.application import interfaces, use_cases
    from server.apps.shortify.application.mappers import ShortLinkMapper
    from server.apps.shortify.domain.constants import ENCODING_ALPHABET
    from server.apps.shortify.infrastructure import services
    from server.apps.shortify.infrastructure.db import (
        mappers,
        repositories,
        transaction,
    )
    from server.apps.shortify.presentation.api.rest.v1.mappers import (
        ShortLinkPresentationMapper,
    )

    # Hacks to resolve annotations:
    inject = _create_injector(container, locals())  # noqa: WPS421

    # Things to register:

    container.register(
        interfaces.transaction.TransactionProtocol,
        transaction.TransactionAtomic,
    )

    # Mappers:
    container.register(ShortLinkPresentationMapper)
    container.register(
        interfaces.mappers.EntityDtoShortLinkMapperProtocol,
        ShortLinkMapper,
    )
    container.register(mappers.ShortLinkDBMapper)

    # Repositories:
    container.register(
        interfaces.repositories.ShortLinkRepositoryProtocol,
        repositories.ShortLinkRepository,
    )
    container.register(
        interfaces.repositories.ClickEventRepositoryProtocol,
        repositories.ClickEventRepository,
    )

    # Services:
    container.register(
        interfaces.services.EncoderProtocol,
        services.Base62EncoderService,
    )
    container.register(
        interfaces.services.ShortLinkGeneratorServiceProtocol,
        inject(services.ShortLinkGeneratorService),
        _alphabet=ENCODING_ALPHABET,
    )
    container.register(
        interfaces.services.GeoResolverServiceProtocol,
        services.GeoIpResolverService,
    )

    # Use cases:
    container.register(inject(use_cases.CreateShortLink))
    container.register(inject(use_cases.GetUrlFromShortLink))


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populates dependencies for the container."""
    # Deps:
    _inject_django(container)
    # Apps:
    _inject_shortify(container)
    return container
