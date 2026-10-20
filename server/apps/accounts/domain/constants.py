from typing import Final

USERNAME_MAX_LENGTH: Final = 150
USERNAME_PATTERN: Final = r'^[\w.@+-]+$'
EMAIL_MAX_LENGTH: Final = 254
EMAIL_PATTERN: Final = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
PASSWORD_MIN_LENGTH: Final = 8
PASSWORD_MAX_LENGTH: Final = 128
