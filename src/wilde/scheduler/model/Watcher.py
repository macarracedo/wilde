from dataclasses import dataclass

from wilde.scheduler.model.Schedule import Schedule
from wilde.operation.Operation import Operation
from wilde.plugin.Plugin import Plugin


# This implementation of watcher only supports one plugin and one operation per watcher.
# This is a limitation that can be improved in the future.
@dataclass(frozen=True)
class Watcher:
    plugin_id: str
    operation: Operation
    schedule: Schedule

    def __str__(self):
        return f"Watcher with operation {self.operation} with plugin_id {self.plugin_id} and schedule {self.schedule})"
    
    def __repr__(self):
        return f"(operation={self.operation}, plugin_id={self.plugin_id}, schedule={self.schedule})"
