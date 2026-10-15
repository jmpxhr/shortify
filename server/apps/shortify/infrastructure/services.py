import uuid
from dataclasses import dataclass
from typing import LiteralString, final, override

from server.apps.shortify.application.interfaces.services import (
    EncoderProtocol,
    ShortLinkGeneratorServiceProtocol,
)

_BASE_NUMBER = 62


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class Base62EncoderService(EncoderProtocol):
    @override
    def __call__(self, *, alphabet: str, number: int) -> str:
        if number == 0:
            return alphabet[0]
        out = []
        while number:
            number, rem = divmod(number, _BASE_NUMBER)
            out.append(alphabet[rem])
        return ''.join(reversed(out))


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ShortLinkGeneratorService(ShortLinkGeneratorServiceProtocol):
    _alphabet: LiteralString
    _encoder: EncoderProtocol

    @override
    def generate_code(self, *, length: int) -> str:
        code = self._encoder(alphabet=self._alphabet, number=uuid.uuid4().int)
        return code[:length]
