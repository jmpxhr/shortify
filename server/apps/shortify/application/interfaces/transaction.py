from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Protocol


class TransactionProtocol(Protocol):
    @abstractmethod
    def __call__(self) -> AbstractContextManager[None]: ...
