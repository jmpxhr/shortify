from collections.abc import Callable
from typing import Any

import punq


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


def inject_shortify(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    _inject_mappers(container)
    _inject_repositories(container)
    _inject_services(container, inject=inject)
    _inject_use_cases(container, inject=inject)
