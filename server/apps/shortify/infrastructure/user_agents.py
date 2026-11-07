from dataclasses import dataclass
from typing import final, override

from user_agents import parse as parse_user_agent
from user_agents.parsers import UserAgent

from server.apps.shortify.application.dtos.click_event import ClickAgentDTO
from server.apps.shortify.application.interfaces.services import (
    UserAgentParserProtocol,
)

_UNKNOWN_FAMILY = 'Other'


@final
@dataclass(frozen=True, slots=True)
class UserAgentsParserService(UserAgentParserProtocol):
    """Derive device, browser, and OS names from a User-Agent header."""

    @override
    def parse(self, *, user_agent: str | None) -> ClickAgentDTO:
        if not user_agent:
            return ClickAgentDTO()

        parsed = parse_user_agent(user_agent)
        return ClickAgentDTO(
            device_type=self._device_type(parsed),
            browser=self._family(parsed.browser.family),
            os=self._family(parsed.os.family),
        )

    def _device_type(self, parsed: UserAgent) -> str:
        if parsed.is_bot:
            return 'bot'
        if parsed.is_tablet:
            return 'tablet'
        if parsed.is_mobile:
            return 'mobile'
        if parsed.is_pc:
            return 'desktop'
        return 'other'

    def _family(self, family: str) -> str | None:
        if family == _UNKNOWN_FAMILY:
            return None
        return family
