from dataclasses import dataclass
from datetime import datetime
from typing import final

from server.apps.shortify.domain.constants import ORIGINAL_URL_MAX_LENGTH


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkEntity:
    original_url: str
    short_code: str
    create_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate entity fields after initialization."""
        if len(self.original_url) == 0:
            raise ValueError('original_url cannot be empty')

        if len(self.original_url) > ORIGINAL_URL_MAX_LENGTH:
            raise ValueError(
                f'original_url is too long. Maximum allowed length is '
                f'{ORIGINAL_URL_MAX_LENGTH} characters '
                f'(got {len(self.original_url)})',
            )

        if not self.original_url.startswith(('http://', 'https://')):
            raise ValueError(
                'original_url must start with http:// or https://',
            )
