import math
from dataclasses import dataclass
from typing import final

from dmr.pagination import Page, Paginated

from server.apps.shortify.application.dtos.short_link import (
    ShortLinkDTO,
    ShortLinkPageDTO,
)
from server.apps.shortify.presentation.api.rest.v1.schemas import (
    ShortLinkDetailSchema,
    ShortLinkResponseSchema,
)


@final
@dataclass(frozen=True, slots=True)
class ShortLinkPresentationMapper:
    def __call__(self, *, short_link: ShortLinkDTO) -> ShortLinkResponseSchema:
        return ShortLinkResponseSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
            clicks=short_link.clicks,
        )

    def detail(self, *, short_link: ShortLinkDTO) -> ShortLinkDetailSchema:
        return ShortLinkDetailSchema(
            original_url=short_link.original_url,
            short_code=short_link.short_code,
            clicks=short_link.clicks,
            created_at=short_link.created_at,
        )

    def page(
        self,
        *,
        page: ShortLinkPageDTO,
        number: int,
        per_page: int,
    ) -> Paginated[ShortLinkResponseSchema]:
        return Paginated(
            count=page.total,
            num_pages=max(1, math.ceil(page.total / per_page)),
            per_page=per_page,
            page=Page(
                number=number,
                object_list=[
                    self(short_link=short_link) for short_link in page.short_links
                ],
            ),
        )
