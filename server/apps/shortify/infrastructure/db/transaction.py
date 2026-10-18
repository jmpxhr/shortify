from collections.abc import Generator
from contextlib import contextmanager
from typing import final, override

from django.db import transaction

from server.apps.shortify.application.interfaces.transaction import TransactionProtocol


@final
class TransactionAtomic(TransactionProtocol):
    """Provide an atomic transaction as an injectable dependency."""

    @override
    @contextmanager
    def __call__(self) -> Generator[None]:
        """Run the enclosed section in one database transaction."""
        with transaction.atomic():
            yield
