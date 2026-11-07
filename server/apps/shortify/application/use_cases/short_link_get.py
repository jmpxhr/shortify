from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, final

from server.apps.shortify.application.dtos.click_event import ClickContextDTO
from server.apps.shortify.application.exceptions import ShortLinkNotFoundError

if TYPE_CHECKING:
    from server.apps.shortify.application.interfaces.repositories import (
        ClickEventRepositoryProtocol,
        ShortLinkRepositoryProtocol,
    )
    from server.apps.shortify.application.interfaces.services import (
        GeolocationProtocol,
        UserAgentParserProtocol,
    )
    from server.common.transaction import TransactionProtocol

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True)
class GetUrlFromShortLink:
    _repository: ShortLinkRepositoryProtocol
    _event_repository: ClickEventRepositoryProtocol
    _geolocation: GeolocationProtocol
    _user_agent_parser: UserAgentParserProtocol
    _transaction: TransactionProtocol

    def __call__(self, *, short_code: str, context: ClickContextDTO) -> str:
        with self._transaction():
            short_link_entity = self._repository.get_by_code(
                short_code=short_code,
            )
            if short_link_entity is None:
                raise ShortLinkNotFoundError(short_code=short_code)
            self._repository.increment_clicks(short_code=short_code)
        self._record_click(short_link_id=short_link_entity.id, context=context)
        return short_link_entity.original_url

    def _record_click(
        self,
        *,
        short_link_id: int,
        context: ClickContextDTO,
    ) -> None:
        try:
            self._store_click(short_link_id=short_link_id, context=context)
        except Exception:
            logger.exception('Unable to record click event for link %s', short_link_id)

    def _store_click(
        self,
        *,
        short_link_id: int,
        context: ClickContextDTO,
    ) -> None:
        location = self._geolocation.resolve(
            ip_address=context.ip_address,
        )
        agent = self._user_agent_parser.parse(
            user_agent=context.user_agent,
        )
        with self._transaction():
            self._event_repository.create(
                short_link_id=short_link_id,
                country_code=location.country_code if location else None,
                region=location.region if location else None,
                city=location.city if location else None,
                referrer_host=context.referrer,
                device_type=agent.device_type,
                browser=agent.browser,
                os=agent.os,
            )
