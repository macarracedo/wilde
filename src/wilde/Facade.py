from wilde.model import LocationData
from wilde.operation.Operation import Operation
from wilde.plugin.PluginManager import PluginManager
from wilde.scheduler.Scheduler import Scheduler
from wilde.scheduler.model.Monitoring import Monitoring
from wilde.scheduler.model.Watcher import Watcher


class Facade:
    def __init__(self, plugin_manager: PluginManager, scheduler: Scheduler):
        self._plugin_manager: PluginManager = plugin_manager
        self._scheduler: Scheduler = scheduler

    def build_operation(self, plugin_id: str, operation_id: str, params: dict[str, str]) -> Operation:
        plugin = self._plugin_manager.get_plugin(plugin_id)

        return plugin.get_operation(operation_id, params)

    def get_data(self, plugin_id: str, operation_id: str, params: dict[str, str],
                 location_data: str | LocationData) -> LocationData:
        operation = self.build_operation(plugin_id=plugin_id, operation_id=operation_id, params=params)

        if isinstance(location_data, str):
            location_data = LocationData(location=location_data, data={})

        operation.run(location_data=location_data)

        return location_data

    def schedule(self, monitoring: Monitoring) -> Monitoring:
        return self._scheduler.schedule(monitoring)

    def retrieve_whois_info(self, location: LocationData) -> LocationData:
        return self._plugin_manager.get_plugin("whois").get_operation("retrieve", {}).run(location)

    def list_watches(self) -> dict[LocationData, dict[str, dict[str, Watcher]]]:
        return self._scheduler.schedules
