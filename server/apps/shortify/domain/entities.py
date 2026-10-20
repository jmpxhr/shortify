import re
from dataclasses import dataclass
from datetime import datetime
from typing import final

from server.apps.shortify.domain.constants import (
    ORIGINAL_URL_MAX_LENGTH,
    ORIGINAL_URL_PATTERN,
)
from server.apps.shortify.domain.exceptions import DomainValidationError


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkEntity:
    id: int
    original_url: str
    short_code: str
    created_at: datetime
    clicks: int = 0

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

        if re.match(ORIGINAL_URL_PATTERN, self.original_url) is None:
            raise DomainValidationError(
                'original_url must start with http:// or https://',
            )
