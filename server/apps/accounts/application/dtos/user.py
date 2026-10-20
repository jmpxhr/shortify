from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class UserDTO:
    id: int
    username: str
    email: str
