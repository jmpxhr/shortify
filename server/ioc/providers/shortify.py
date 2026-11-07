from collections.abc import Callable
from typing import Any

import punq


def _inject_mappers(container: punq.Container) -> None:
    from server.apps.shortify.application.interfaces.mappers import (
        EntityDtoShortLinkMapperProtocol,
    )
    from server.apps.shortify.application.mappers import ShortLinkMapper
    from server.apps.shortify.infrastructure.mappers import (
        ClickEventDBMapper,
        ShortLinkDBMapper,
    )
    from server.apps.shortify.presentation.api.rest.v1.mappers import (
        ShortLinkPresentationMapper,
    )

    container.register(ShortLinkPresentationMapper)
    container.register(EntityDtoShortLinkMapperProtocol, ShortLinkMapper)
    container.register(ShortLinkDBMapper)
    container.register(ClickEventDBMapper)


def _inject_repositories(container: punq.Container) -> None:
    from server.apps.shortify.application.interfaces.repositories import (
        ClickEventRepositoryProtocol,
        ShortLinkRepositoryProtocol,
    )
    from server.apps.shortify.infrastructure.repositories import (
        ClickEventRepository,
        ShortLinkRepository,
    )

    container.register(ShortLinkRepositoryProtocol, ShortLinkRepository)
    container.register(ClickEventRepositoryProtocol, ClickEventRepository)


def _inject_services(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from django.conf import settings

    from server.apps.shortify.application.interfaces.services import (
        EncoderProtocol,
        GeolocationProtocol,
        ShortLinkGeneratorServiceProtocol,
        UserAgentParserProtocol,
    )
    from server.apps.shortify.domain.constants import ENCODING_ALPHABET
    from server.apps.shortify.infrastructure.geoip import (
        MaxMindGeolocationService,
    )
    from server.apps.shortify.infrastructure.services import (
        Base62EncoderService,
        ShortLinkGeneratorService,
    )
    from server.apps.shortify.infrastructure.user_agents import (
        UserAgentsParserService,
    )

    container.register(EncoderProtocol, Base62EncoderService)
    container.register(
        ShortLinkGeneratorServiceProtocol,
        inject(ShortLinkGeneratorService),
        _alphabet=ENCODING_ALPHABET,
    )
    container.register(
        GeolocationProtocol,
        MaxMindGeolocationService,
        _db_path=settings.GEOIP_PATH,
        scope=punq.Scope.singleton,
    )
    container.register(UserAgentParserProtocol, UserAgentsParserService)


def _inject_use_cases(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from server.apps.shortify.application import use_cases

    container.register(inject(use_cases.CreateShortLink))
    container.register(inject(use_cases.DeleteShortLink))
    container.register(inject(use_cases.GetLinkAnalytics))
    container.register(inject(use_cases.GetShortLink))
    container.register(inject(use_cases.GetUrlFromShortLink))
    container.register(inject(use_cases.ListShortLinks))


def inject_shortify(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    _inject_mappers(container)
    _inject_repositories(container)
    _inject_services(container, inject=inject)
    _inject_use_cases(container, inject=inject)
