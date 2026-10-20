from collections.abc import Sequence
from typing import final


@final
class UserAlreadyExistsError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f'User already exists: {username}')
        self.username = username


@final
class WeakPasswordError(Exception):
    def __init__(self, messages: Sequence[str]) -> None:
        super().__init__('; '.join(messages))
        self.messages = tuple(messages)
