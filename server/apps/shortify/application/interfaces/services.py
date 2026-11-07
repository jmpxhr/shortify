from abc import abstractmethod
from typing import Protocol

from server.apps.shortify.application.dtos.click_event import (
    ClickAgentDTO,
    GeolocationDTO,
)


class EncoderProtocol(Protocol):
    @abstractmethod
    def __call__(self, *, alphabet: str, number: int) -> str: ...


class ShortLinkGeneratorServiceProtocol(Protocol):
    @abstractmethod
    def generate_code(self, *, length: int) -> str: ...


class GeolocationProtocol(Protocol):
    @abstractmethod
    def resolve(self, *, ip_address: str | None) -> GeolocationDTO | None: ...


class UserAgentParserProtocol(Protocol):
    @abstractmethod
    def parse(self, *, user_agent: str | None) -> ClickAgentDTO: ...
