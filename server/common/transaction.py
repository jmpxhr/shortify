from abc import abstractmethod
from collections.abc import Generator
from contextlib import AbstractContextManager, contextmanager
from typing import Protocol, final, override

from django.db import transaction


class TransactionProtocol(Protocol):
    """Protocol for a callable that returns an atomic transaction ctx."""

    @abstractmethod
    def __call__(self) -> AbstractContextManager[None]:
        """Return a context manager that wraps code in an atomic transaction."""


@final
class TransactionAtomic(TransactionProtocol):
    """Provide an atomic transaction as an injectable dependency."""

    @override
    @contextmanager
    def __call__(self) -> Generator[None]:
        """Run the enclosed section in one database transaction."""
        with transaction.atomic():
            yield
