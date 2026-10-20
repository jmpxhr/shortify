from typing import Annotated, final

import msgspec

from server.apps.shortify.domain.constants import (
    ORIGINAL_URL_MAX_LENGTH,
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
                'pattern': '^https?://',
                'example': 'https://github.com/wemake-services/wemake-django-template',
            }
        ),
    ]


@final
class ShortLinkResponseSchema(msgspec.Struct):
    """Schema for a short link API response."""

    original_url: str
    short_code: str


@final
class ShortLinkPath(msgspec.Struct):
    short_code: Annotated[
        str,
        msgspec.Meta(
            max_length=SHORT_URL_MAX_LENGTH,
            pattern=SHORT_CODE_PATTERN,
        ),
    ]
