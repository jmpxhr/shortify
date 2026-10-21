from collections.abc import Sequence
from typing import final


@final
class UserAlreadyExistsError(Exception):
    """Raised when a user with the same username already exists."""

    def __init__(self, username: str) -> None:
        super().__init__(f'User already exists: {username}')
        self.username = username


@final
class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""

    def __init__(self, user_id: int) -> None:
        super().__init__(f'User not found: {user_id}')
        self.user_id = user_id


@final
class WeakPasswordError(Exception):
    """Raised when the provided password fails validation."""

    def __init__(self, messages: Sequence[str]) -> None:
        super().__init__('; '.join(messages))
        self.messages = tuple(messages)
