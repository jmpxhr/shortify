from abc import abstractmethod
from typing import Protocol


class EncoderProtocol(Protocol):
    @abstractmethod
    def __call__(self, *, alphabet: str, number: int) -> str: ...
