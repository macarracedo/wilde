import dataclasses
import time
from datetime import datetime
from threading import Thread, Event
from typing import Optional, Type

import schedule
from sqlalchemy import Engine

from wilde.database.MonitoringDAO import MonitoringDAO
from wilde.database.LocationDataDAO import LocationDataDAO
from wilde.database.entity.MonitoringEntity import MonitoringEntity
from wilde.database.entity.LocationEntity import LocationEntity
from wilde.model import LocationData
from wilde.operation.Operation import Operation
from wilde.scheduler.model.Monitoring import Monitoring
from wilde.scheduler.model.Schedule import Schedule
from wilde.scheduler.model.Watcher import Watcher


class Scheduler:
    def __init__(self, engine: Engine, check_interval: int = 1, start: bool = False):
        self._engine: Engine = engine
        self._check_interval: int = check_interval
        self._check_is_active: Event = Event()
        self._check_thread: Optional[Thread] = None

        self._scheduler: schedule.Scheduler = schedule.Scheduler()
        self._schedules: dict[LocationData, dict[str, dict[str, Watcher]]] = {}

        if start:
            self.start()

    @property
    def schedules(self) -> dict[LocationData, dict[str, dict[str, Watcher]]]:
        return self._schedules.copy()

    def start(self) -> None:
        if not self._check_is_active.is_set():
            self._check_thread = Thread(target=self._check_tasks, daemon=True)
            self._check_is_active.set()
            self._check_thread.start()

    def stop(self) -> None:
        if self._check_is_active.is_set():
            self._check_is_active.clear()

            if self._check_thread is None:
                raise AttributeError("self._check_thread should not be None")

            self._check_thread.join()
            self._check_thread = None

    def _check_tasks(self) -> None:
        while self._check_is_active.is_set():
            self._scheduler.run_pending()
            time.sleep(self._check_interval)

    def _operation_runner_persist(self, operation: Operation, location_data: LocationData) -> None:
        location_data = operation.run(location_data)
        ld_dao = LocationDataDAO(self._engine)
        ld_dao.persist(LocationEntity(location_data))

    def _run_task(self, operation: Operation, location_data: LocationData) -> None:
        task_thread = Thread(target=self._operation_runner_persist, args=(operation, location_data,))
        task_thread.start()

    def _schedule_task(self, operation: Operation, location_data: LocationData, task_schedule: Schedule) -> None:
        if task_schedule.start is None:
            self._run_task(operation, location_data)

            # No need to save the returned job, as it is already saved in the scheduler
            self._scheduler.every(task_schedule.interval).seconds.do(self._run_task,
                                                                     operation=operation,
                                                                     location_data=location_data)
        else:
            def delayed_start() -> Type[schedule.CancelJob]:
                self._schedule_task(operation, location_data, dataclasses.replace(task_schedule, start=None))
                return schedule.CancelJob

            start = datetime.fromtimestamp(task_schedule.start)
            now = datetime.now()

            self._scheduler.every(int((start - now).total_seconds())).seconds.do(delayed_start)

    # Save current schedule dict to database
    def _persist(self, monitoring: Monitoring) -> None:
        mon_dao = MonitoringDAO(self._engine)
        mon_dao.persist(MonitoringEntity(monitoring))

    def schedule(self, monitoring: Monitoring) -> Monitoring:
        location_data = monitoring.location_data

        # TODO: check if location already has watchers
        self._schedules[location_data] = {}
        self._persist(monitoring)

        for watcher in monitoring.watchers:
            plugin_id = watcher.operation.plugin_id()
            operation_id = watcher.operation.id()

            if plugin_id not in self._schedules[location_data]:
                self._schedules[location_data][plugin_id] = {
                    operation_id: watcher
                }
            else:
                self._schedules[location_data][plugin_id][operation_id] = watcher

            self._schedule_task(watcher.operation, location_data, watcher.schedule)

        return monitoring
