from collections.abc import Callable
from typing import Any

import punq

from server.ioc.providers.accounts import inject_accounts
from server.ioc.providers.django import inject_django
from server.ioc.providers.shortify import inject_shortify
from server.ioc.providers.transaction import inject_transaction


def _global_namespace() -> dict[str, Any]:
    from django.conf import LazySettings
    from django.core.cache import BaseCache

    return locals()  # noqa: WPS421


def _create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    # We need to provide the same string names as we do in the definition.
    localns.pop('container')
    localns.update(_global_namespace())
    # pyrefly: ignore [missing-attribute]
    # ruff: ignore[private-member-access]
    container.registrations._localns.update(localns)
    return lambda service: service


def populate_dependencies(container: punq.Container) -> punq.Container:
    """Populates dependencies for the container."""

    # Hacks to resolve annotations:
    inject = _create_injector(container, locals())  # noqa: WPS421

    # Deps:
    inject_django(container, inject=inject)
    inject_transaction(container, inject=inject)

    # Apps:
    inject_shortify(container, inject=inject)
    inject_accounts(container, inject=inject)
    return container
