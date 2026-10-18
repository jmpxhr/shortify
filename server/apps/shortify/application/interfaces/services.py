from abc import abstractmethod
from typing import Protocol


class EncoderProtocol(Protocol):
    @abstractmethod
    def __call__(self, *, alphabet: str, number: int) -> str: ...


class ShortLinkGeneratorServiceProtocol(Protocol):
    @abstractmethod
    def generate_code(self, *, length: int) -> str: ...


class GeoResolverServiceProtocol(Protocol):
    @abstractmethod
    def resolve_country(self, *, ip: str | None) -> str | None: ...
