from dataclasses import dataclass
from datetime import datetime
from typing import final

from server.apps.shortify.domain.constants import ORIGINAL_URL_MAX_LENGTH
from server.apps.shortify.domain.exceptions import DomainValidationError


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkEntity:
    original_url: str
    short_code: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate entity fields after initialization."""
        if len(self.original_url) == 0:
            raise DomainValidationError('original_url cannot be empty')

        if len(self.original_url) > ORIGINAL_URL_MAX_LENGTH:
            raise DomainValidationError(
                f'original_url is too long. Maximum allowed length is '
                f'{ORIGINAL_URL_MAX_LENGTH} characters '
                f'(got {len(self.original_url)})',
            )

        if not self.original_url.startswith(('http://', 'https://')):
            raise DomainValidationError(
                'original_url must start with http:// or https://',
            )
