from dataclasses import dataclass
from typing import final

from django.db import IntegrityError

from server.apps.shortify.application.exceptions import ShortLinkCollisionError
from server.apps.shortify.infrastructure.models import ShortLink


@final
@dataclass(frozen=True, slots=True)
class ShortLinkRepository:
    def create(self, *, original_url: str, short_code: str) -> ShortLink:
        try:
            return ShortLink.objects.create(
                original_url=original_url, short_code=short_code
            )
        except IntegrityError as exc:
            raise ShortLinkCollisionError(short_code) from exc

    def get_by_code(self, *, short_code: str) -> ShortLink | None:
        try:
            return ShortLink.objects.get(short_code=short_code)
        except ShortLink.DoesNotExist:
            return None
