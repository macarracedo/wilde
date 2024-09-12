from enum import Enum
from typing import Optional

from validators import url, domain, ip_address


class LocationType(Enum):
    IP = 'ip'
    URL = 'url'
    DOMAIN = 'domain'


class LocationData:
    """
    Class that contains an Internet location (URL, domain or IP) and metadata associated to this class.
    """

    def __init__(self, location: str, data: dict[str, str], location_domain: Optional[str] = None,
                 ip: Optional[str] = None):
        if not isinstance(location, str):
            raise TypeError("location must be a str")
        if not isinstance(data, dict):
            raise TypeError("data must be a dict[str, str]")

        self._location: str = location
        self._data: dict[str, str] = data
        self._location_type: LocationType = self._get_location_type(location)
        self._domain: Optional[str] = location_domain
        self._ip: Optional[str] = ip

    @property
    def location(self) -> str:
        return self._location

    @property
    def data(self) -> dict[str, str]:
        return self._data.copy()

    @property
    def location_type(self) -> LocationType:
        return self._location_type

    @property
    def domain(self) -> Optional[str]:
        return self._domain

    @property
    def ip(self) -> Optional[str]:
        return self._ip

    def is_a(self, location_type: LocationType) -> bool:
        return self._location_type == location_type

    @staticmethod
    def _get_location_type(location: str) -> LocationType:
        # Check if it's a valid IP address
        if ip_address.ipv4(location):
            return LocationType.IP

        # Check if it's a valid URL
        if url(location):
            return LocationType.URL

        # Check if it's a valid domain
        if domain(location):
            return LocationType.DOMAIN

        raise ValueError('Invalid location given', location)

    def has_data_key(self, key: str) -> bool:
        return key in self._data

    def get_data_value(self, key: str) -> str:
        return self._data.get(key, "")

    def set_data_value(self, key: str, value: str) -> None:
        self._data[key] = value

    def remove_data_key(self, key: str) -> None:
        if key in self._data:
            del self._data[key]

    def clear_data(self) -> None:
        self._data.clear()

    def __str__(self) -> str:
        return f"LocationData with location {self._location}, and data {self._data})"

    def __repr__(self) -> str:
        return f"({self._location}, {self._data})"
