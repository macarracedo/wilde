from typing import TypedDict

from wilde.model import LocationData


class MappedLocationData(TypedDict):
    location: str
    data: dict[str, str]


class LocationDataMapper:
    def map(self, location: LocationData) -> MappedLocationData:
        return {
            "location": location.location,
            "data": location.data
        }
