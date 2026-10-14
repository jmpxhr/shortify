# NOTE: simple layers go on top!

import string
from collections.abc import Callable
from typing import Any

import punq


def _global_namespace() -> dict[str, Any]:
    from django.conf import LazySettings
    from django.core.cache import BaseCache

    return locals()


def _create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    # We need to provide the same string names as we do in the definition.
    localns.pop('container')
    localns.update(_global_namespace())
    # pyrefly: ignore [missing-attribute]
    container.registrations._localns.update(localns)  # ruff: ignore[private-member-access]
    return lambda service: service


def _inject_django(container: punq.Container) -> None:
    from django.conf import LazySettings, settings

    # Django:
    container.register(
        LazySettings,
        instance=settings,
        scope=punq.Scope.singleton,
    )


def _inject_shortify(container: punq.Container) -> None:
    from server.apps.shortify.api import mappers as api_mappers
    from server.apps.shortify.domain import interfaces, services, use_case
    from server.apps.shortify.domain.constants import ENCODING_ALPHABET
    from server.apps.shortify.infrastructure import mappers, repositories

    # Hacks to resolve annotations:
    inject = _create_injector(container, locals())

    # Things to register:
    # Mappers:
    container.register(mappers.ShortLinkMapper)
    container.register(api_mappers.ShortLinkDtoMapper)
    # Repositories:
    container.register(repositories.ShortLinkRepository)
    # Services:
    container.register(interfaces.EncoderProtocol, services.Base62EncoderService)
    container.register(
        inject(services.ShortLinkGeneratorService),
        _alphabet=ENCODING_ALPHABET,
    )
    # Use cases:
    container.register(inject(use_case.CreateShortLink))
    container.register(inject(use_case.GetUrlFromShortLink))


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populates dependencies for the container."""
    # Deps:
    _inject_django(container)
    # Apps:
    _inject_shortify(container)
    return container
