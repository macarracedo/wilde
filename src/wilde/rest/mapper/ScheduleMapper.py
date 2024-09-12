from typing import TypedDict

from wilde.Facade import Facade
from wilde.model import LocationData
from wilde.rest.mapper.MonitoringConfigurationMapper import ScheduleConfiguration
from wilde.scheduler.model.Watcher import Watcher


class LocationWatch(TypedDict):
    location_data: str
    watchers: dict[str, dict[str, ScheduleConfiguration]]


class ScheduleMapper:

    def map(self, schedule: dict[LocationData, dict[str, dict[str, Watcher]]]) -> list[LocationWatch]:
        mapped_schedules: list[LocationWatch] = []

        for location_data, watches in schedule.items():
            mapped_watchers: dict[str, dict[str, ScheduleConfiguration]] = {}

            for plugin_id, operation_watches in watches.items():
                if plugin_id not in mapped_watchers:
                    mapped_watchers[plugin_id] = {}

                for operation_id, watcher in operation_watches.items():
                    mapped_schedule: ScheduleConfiguration = {
                        "interval": watcher.schedule.interval
                    }
                    if watcher.schedule.start is not None:
                        mapped_schedule["start"] = watcher.schedule.start

                    mapped_watchers[plugin_id][operation_id] = mapped_schedule

            mapped_location_watches: LocationWatch = {
                "location_data": location_data.location,
                "watchers": mapped_watchers
            }

            mapped_schedules.append(mapped_location_watches)

        return mapped_schedules
