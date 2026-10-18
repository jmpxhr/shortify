import string
from typing import Final

ORIGINAL_URL_MAX_LENGTH: Final = 200
SHORT_URL_MAX_LENGTH: Final = 10
SHORT_CODE_LENGTH: Final = 6
ENCODING_ALPHABET: Final = string.ascii_letters + string.digits

MAX_REFERER_LENGTH: Final = 512
MAX_USER_AGENT_LENGTH: Final = 512
