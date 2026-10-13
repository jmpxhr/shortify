from http import HTTPStatus
from typing import final, override

from django.http import HttpResponse
from dmr import Body, Controller, ResponseSpec, modify
from dmr.endpoint import Endpoint
from dmr.errors import ErrorType
from dmr.plugins.msgspec import MsgspecSerializer

from server.apps.shortify.api import mappers
from server.apps.shortify.api.schemas import (
    ShortLinkCreateSchema,
    ShortLinkResponseSchema,
)
from server.apps.shortify.domain import use_case
from server.apps.shortify.domain.exceptions import ShortLinkCollisionError
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
