from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, HeaderSpec, Path, RedirectTo, ResponseSpec, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import MsgspecSerializer

from server.apps.shortify.domain import use_case
from server.apps.shortify.domain.exceptions import (
    ShortLinkCollisionError,
    ShortLinkNotFoundError,
)
from server.apps.shortify.domain.use_case.short_link_get import GetUrlFromShortLink
from server.apps.shortify.presentation.api.rest import mappers
from server.apps.shortify.presentation.api.rest.schemas import (
    ShortLinkCreateSchema,
    ShortLinkPath,
    ShortLinkResponseSchema,
)
from server.common.di import HasContainer


@final
class ShortLinkView(HasContainer, Controller[MsgspecSerializer]):
    description = 'Short Link View'

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
        parsed_body: Body[ShortLinkCreateSchema],
    ) -> ShortLinkResponseSchema:
        return self.resolve(mappers.ShortLinkDtoMapper)(
            short_link=self.resolve(use_case.CreateShortLink)(
                original_url=parsed_body.original_url
            )
        )

    @override
    def handle_error(
        self,
        endpoint: Endpoint,
        controller: Controller[MsgspecSerializer],
        exc: Exception,
    ) -> HttpResponse:
        if isinstance(exc, ValueError):
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
class RedirectView(HasContainer, Controller[MsgspecSerializer]):
    description = 'Redirect Controller'

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
