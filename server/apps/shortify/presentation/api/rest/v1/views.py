from http import HTTPStatus
from typing import final, override

from django.contrib.auth.models import User
from django.http import HttpResponse
from dmr import (
    Controller,
    HeaderSpec,
    Path,
    Query,
    RedirectTo,
    ResponseSpec,
    modify,
)
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.pagination import Paginated
from dmr.plugins.msgspec import BodyMsgspec, MsgspecSerializer
from dmr.security import AuthenticatedHttpRequest

from server.apps.shortify.application import use_cases
from server.apps.shortify.application.exceptions import (
    ShortLinkCollisionError,
    ShortLinkNotFoundError,
)
from server.apps.shortify.application.use_cases.short_link_get import (
    GetUrlFromShortLink,
)
from server.apps.shortify.domain.exceptions import DomainValidationError
from server.apps.shortify.presentation.api.rest.v1 import mappers
from server.apps.shortify.presentation.api.rest.v1.schemas import (
    ShortLinkCreateSchema,
    ShortLinkDetailSchema,
    ShortLinkListQuery,
    ShortLinkPath,
    ShortLinkResponseSchema,
)
from server.common.di import HasContainer


@final
class ShortLinkView(HasContainer, Controller[MsgspecSerializer]):
    description = 'Short Link View'
    request: AuthenticatedHttpRequest[User]  # pyrefly: ignore [bad-override-mutable-attribute]

    def get(
        self,
        parsed_query: Query[ShortLinkListQuery],
    ) -> Paginated[ShortLinkResponseSchema]:
        """List my short links."""
        page_dto = self.resolve(use_cases.ListShortLinks)(
            owner_id=self.request.user.pk,
            page=parsed_query.page,
            page_size=parsed_query.page_size,
        )
        return self.resolve(mappers.ShortLinkPresentationMapper).page(
            page=page_dto,
            number=parsed_query.page,
            per_page=parsed_query.page_size,
        )

    @modify(
        extra_responses=[
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.BAD_REQUEST,
            ),
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.CONFLICT,
            ),
        ]
    )
    def post(
        self,
        parsed_body: BodyMsgspec[ShortLinkCreateSchema],
    ) -> ShortLinkResponseSchema:
        """Create short link"""

        short_link_dto = self.resolve(use_cases.CreateShortLink)(
            original_url=parsed_body.original_url,
            owner_id=self.request.user.pk,
        )
        return self.resolve(mappers.ShortLinkPresentationMapper)(
            short_link=short_link_dto
        )

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, DomainValidationError):
            return self.to_error(
                self.format_error(
                    str(exc),
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.BAD_REQUEST,
            )

        if isinstance(exc, ShortLinkCollisionError):
            return self.to_error(
                self.format_error(
                    'Failed to generate a unique short code, please retry',
                    error_type=ErrorType.value_error,
                ),
                status_code=HTTPStatus.CONFLICT,
            )
        return super().handle_error(endpoint, controller, exc)


@final
class ShortLinkDetailView(HasContainer, Controller[MsgspecSerializer]):
    """Read or delete one of the authenticated user's links."""

    description = 'Short link detail.'
    request: AuthenticatedHttpRequest[User]  # pyrefly: ignore [bad-override-mutable-attribute]

    @modify(
        extra_responses=[
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.NOT_FOUND,
            ),
        ],
    )
    def get(self, parsed_path: Path[ShortLinkPath]) -> ShortLinkDetailSchema:
        """Return my link's detail."""
        short_link_dto = self.resolve(use_cases.GetShortLink)(
            short_code=parsed_path.short_code,
            owner_id=self.request.user.pk,
        )
        return self.resolve(mappers.ShortLinkPresentationMapper).detail(
            short_link=short_link_dto,
        )

    @modify(
        status_code=HTTPStatus.NO_CONTENT,
        extra_responses=[
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.NOT_FOUND,
            ),
        ],
    )
    def delete(self, parsed_path: Path[ShortLinkPath]) -> None:
        """Delete one of my links."""
        self.resolve(use_cases.DeleteShortLink)(
            short_code=parsed_path.short_code,
            owner_id=self.request.user.pk,
        )

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, ShortLinkNotFoundError):
            return self.to_error(
                self.format_error(
                    'Link not found',
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)


@final
class RedirectView(HasContainer, Controller[MsgspecSerializer]):
    description = 'Redirect Controller'
    auth = None

    @modify(
        extra_responses=[
            ResponseSpec(
                None,
                status_code=HTTPStatus.FOUND,
                headers={'Location': HeaderSpec()},
            ),
            ResponseSpec(
                Controller.error_model,
                status_code=HTTPStatus.NOT_FOUND,
            ),
        ],
    )
    def get(self, parsed_path: Path[ShortLinkPath]) -> None:
        original_url = self.resolve(GetUrlFromShortLink)(
            short_code=parsed_path.short_code,
        )
        raise RedirectTo(original_url, status_code=HTTPStatus.FOUND)

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, ShortLinkNotFoundError):
            return self.to_error(
                self.format_error(
                    'Link not found',
                    error_type=ErrorType.not_found,
                ),
                status_code=HTTPStatus.NOT_FOUND,
            )
        return super().handle_error(endpoint, controller, exc)
