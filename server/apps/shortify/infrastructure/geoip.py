from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import final, override

from geoip2 import database as geoip_database
from geoip2 import errors as geoip_errors

from server.apps.shortify.application.dtos.click_event import GeolocationDTO
from server.apps.shortify.application.interfaces.services import GeolocationProtocol

logger = logging.getLogger(__name__)


@final
@dataclass(slots=True)
class MaxMindGeolocationService(GeolocationProtocol):
    """Resolve click locations from a local MaxMind GeoLite2 database."""

    _db_path: str
    _reader: geoip_database.Reader | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _unavailable: bool = field(default=False, init=False, repr=False)

    @override
    def resolve(self, *, ip_address: str | None) -> GeolocationDTO | None:
        if not ip_address:
            return None

        reader = self._get_reader()
        if reader is None:
            return None

        try:
            response = reader.city(ip_address)
        except geoip_errors.AddressNotFoundError, ValueError:
            return None

        return GeolocationDTO(
            country_code=response.country.iso_code,
            region=response.subdivisions.most_specific.name,
            city=response.city.name,
        )

    def _get_reader(self) -> geoip_database.Reader | None:
        if self._reader is not None:
            return self._reader
        if self._unavailable:
            return None

        database_path = Path(self._db_path)
        if not database_path.is_file():
            logger.warning(
                'GeoIP database not found at %s; geolocation is unknown',
                database_path,
            )
            self._unavailable = True
            return None

        try:
            self._reader = geoip_database.Reader(database_path)
        except (OSError, geoip_errors.GeoIP2Error) as exc:
            logger.warning(
                'Unable to open GeoIP database at %s: %s',
                database_path,
                exc,
            )
            self._unavailable = True
            return None
        return self._reader
