from abc import abstractmethod
from typing import Protocol

from server.apps.shortify.application.dtos.short_link import ShortLinkDTO
from server.apps.shortify.domain.entities import ShortLinkEntity


class EntityDtoShortLinkMapperProtocol(Protocol):
    @abstractmethod
    def to_dto(self, entity: ShortLinkEntity) -> ShortLinkDTO: ...
