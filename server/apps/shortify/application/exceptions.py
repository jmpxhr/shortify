from typing import final


@final
class ShortLinkNotFoundError(Exception):
    """Raised when a short link cannot be found."""

    def __init__(self, short_code: str) -> None:
        super().__init__(f'Short link not found: {short_code}')
        self.short_code = short_code


@final
class ShortLinkCollisionError(Exception):
    """Raised when a generated short code is already taken."""

    def __init__(self, short_code: str) -> None:
        super().__init__(f'Short code collision: {short_code}')
        self.short_code = short_code
