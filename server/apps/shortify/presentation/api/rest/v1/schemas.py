from datetime import datetime
from typing import Annotated, final

import msgspec

from server.apps.shortify.domain.constants import (
    ORIGINAL_URL_MAX_LENGTH,
    ORIGINAL_URL_PATTERN,
    SHORT_CODE_PATTERN,
    SHORT_URL_MAX_LENGTH,
)


@final
class ShortLinkCreateSchema(msgspec.Struct):
    original_url: Annotated[
        str,
        msgspec.Meta(
            extra_json_schema={
                'minLength': 1,
                'maxLength': ORIGINAL_URL_MAX_LENGTH,
                'pattern': ORIGINAL_URL_PATTERN,
                'example': 'https://github.com/wemake-services/wemake-django-template',
            }
        ),
    ]


@final
class ShortLinkResponseSchema(msgspec.Struct):
    """Schema for a short link API response."""

    original_url: Annotated[
        str,
        msgspec.Meta(
            examples=['https://github.com/wemake-services/wemake-django-template'],
        ),
    ]
    short_code: Annotated[
        str,
        msgspec.Meta(examples=['aB3xY9']),
    ]
    clicks: Annotated[
        int,
        msgspec.Meta(examples=[3]),
    ]


@final
class ShortLinkDetailSchema(msgspec.Struct):
    """Schema for a short link detail API response."""

    original_url: Annotated[
        str,
        msgspec.Meta(
            examples=['https://github.com/wemake-services/wemake-django-template'],
        ),
    ]
    short_code: Annotated[
        str,
        msgspec.Meta(examples=['aB3xY9']),
    ]
    clicks: Annotated[
        int,
        msgspec.Meta(examples=[3]),
    ]
    created_at: Annotated[
        datetime,
        msgspec.Meta(examples=['2026-10-21T09:35:00Z']),
    ]


@final
class ShortLinkListQuery(msgspec.Struct):
    """Query parameters for listing the current user's short links."""

    page: Annotated[
        int,
        msgspec.Meta(ge=1, examples=[1]),
    ] = 1
    page_size: Annotated[
        int,
        msgspec.Meta(ge=1, le=100, examples=[20]),
    ] = 20


@final
class ShortLinkPath(msgspec.Struct):
    short_code: Annotated[
        str,
        msgspec.Meta(
            max_length=SHORT_URL_MAX_LENGTH,
            pattern=SHORT_CODE_PATTERN,
        ),
    ]
