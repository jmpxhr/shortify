from typing import final


@final
class UserValidationError(Exception):
    """Raised when a user entity fails domain validation."""
