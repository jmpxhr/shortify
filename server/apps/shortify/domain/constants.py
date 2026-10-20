import string
from typing import Final

ORIGINAL_URL_MAX_LENGTH: Final = 200
SHORT_URL_MAX_LENGTH: Final = 10
SHORT_CODE_LENGTH: Final = 6
SHORT_CODE_MAX_ATTEMPTS: Final = 5
ENCODING_ALPHABET: Final = string.ascii_letters + string.digits
SHORT_CODE_PATTERN: Final = '^[a-zA-Z0-9]+$'
