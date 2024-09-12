from typing import TypedDict, List

from wilde.Facade import Facade
from wilde.model import LocationData
from wilde.scheduler.model.Monitoring import Monitoring
from wilde.scheduler.model.Schedule import Schedule
from wilde.scheduler.model.Watcher import Watcher


class ScheduleConfiguration(TypedDict, total=False):
    interval: int
    start: int | None


class OperationConfiguration(TypedDict):
    params: dict[str, str]
    schedule: ScheduleConfiguration


class MonitoringConfiguration(TypedDict):
    location: str
    watchers: dict[str, dict[str, OperationConfiguration]]


class MonitoringConfigurationMapper:
    def __init__(self, facade: Facade):
        self._facade: Facade = facade

    def map(self, configuration: MonitoringConfiguration) -> Monitoring:
        location_data = LocationData(location=configuration["location"], data={})
        watchers: List[Watcher] = []

        for plugin_id, watcher_config in configuration["watchers"].items():
            for operation_id, operation_config in watcher_config.items():
                params = operation_config["params"]
                operation = self._facade.build_operation(plugin_id, operation_id, params)

                schedule_config = operation_config["schedule"]
                interval = schedule_config["interval"]
                start = schedule_config["start"] if "start" in schedule_config else None
                schedule = Schedule(interval, start)

                watchers.append(Watcher(plugin_id, operation, schedule))

        return Monitoring(location_data, watchers)
