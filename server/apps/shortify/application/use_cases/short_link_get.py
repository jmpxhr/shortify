from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.dtos.click_event import ClickContext
from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.repositories import (
        ClickEventRepositoryProtocol,
        ShortLinkRepositoryProtocol,
    )
    from server.apps.shortify.application.interfaces.services import (
        GeoResolverServiceProtocol,
    )
    from server.apps.shortify.application.interfaces.transaction import (
        TransactionProtocol,
    )


@final
@dataclass(frozen=True, slots=True)
class GetUrlFromShortLink:
    _repository: ShortLinkRepositoryProtocol
    _click_event_repository: ClickEventRepositoryProtocol
    _geo_resolver: GeoResolverServiceProtocol
    _transaction: TransactionProtocol

    def __call__(
        self,
        *,
        short_code: str,
        click_context: ClickContext | None = None,
    ) -> str:
        with self._transaction():
            short_link_entity = self._repository.get_by_code(short_code=short_code)
            if short_link_entity is None:
                raise ShortLinkNotFoundError(short_code=short_code)
            if click_context is not None:
                country = self._geo_resolver.resolve_country(ip=click_context.ip)
                self._click_event_repository.record_click(
                    short_code=short_code,
                    referer=click_context.referer,
                    user_agent=click_context.user_agent,
                    country=country,
                )
            self._repository.increment_clicks(short_code=short_code)
        return short_link_entity.original_url
