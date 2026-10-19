from abc import abstractmethod
from contextlib import AbstractContextManager
from typing import Protocol


class TransactionProtocol(Protocol):
    """Protocol for a callable that returns an atomic transaction ctx."""

    @abstractmethod
    def __call__(self) -> AbstractContextManager[None]:
        """Return a context manager that wraps code in an atomic transaction."""
