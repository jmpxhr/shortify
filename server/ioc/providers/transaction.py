from collections.abc import Callable
from typing import Any

import punq


def inject_transaction(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from server.common.transaction import TransactionAtomic, TransactionProtocol

    container.register(TransactionProtocol, TransactionAtomic)
