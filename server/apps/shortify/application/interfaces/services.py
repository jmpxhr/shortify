from abc import abstractmethod
from typing import Protocol


class EncoderProtocol(Protocol):
    @abstractmethod
    def __call__(self, *, alphabet: str, number: int) -> str: ...


class ShortLinkGeneratorServiceProtocol(Protocol):
    @abstractmethod
    def generate_code(self, *, length: int) -> str: ...
