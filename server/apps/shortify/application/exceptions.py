from typing import final


@final
class ShortLinkNotFoundError(Exception):
    def __init__(self, short_code: str) -> None:
        super().__init__(f'Short link not found: {short_code}')
        self.short_code = short_code


@final
class ShortLinkCollisionError(Exception):
    def __init__(self, short_code: str) -> None:
        super().__init__(f'Short code collision: {short_code}')
        self.short_code = short_code
