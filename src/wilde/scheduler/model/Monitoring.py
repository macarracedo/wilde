from typing import List

from wilde.model import LocationData
from wilde.scheduler.model.Watcher import Watcher


class Monitoring:
    def __init__(self, location_data: LocationData, watchers: List[Watcher]):
        self._location_data: LocationData = location_data
        self._watchers: List[Watcher] = [] if watchers is None else watchers.copy()

    @property
    def location_data(self) -> LocationData:
        return self._location_data

    @property
    def watchers(self) -> List[Watcher]:
        return self._watchers.copy()

    def __str__(self):
        return f"Monitoring for location {self._location_data.data} with watchers {self._watchers})"
    
    def __repr__(self):
        return f"(location_data={self._location_data}, watchers={self._watchers})"
