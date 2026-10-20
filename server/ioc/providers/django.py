from collections.abc import Callable
from typing import Any

import punq


def inject_django(
    container: punq.Container,
    *,
    inject: Callable[[Any], Any],
) -> None:
    from django.conf import LazySettings, settings

    # Django:
    container.register(
        LazySettings,
        instance=settings,
        scope=punq.Scope.singleton,
    )
