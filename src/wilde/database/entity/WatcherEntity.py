from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from wilde.database.entity import Base
from wilde.database.entity.ScheduleEntity import ScheduleEntity
from wilde.scheduler.model.Watcher import Watcher

if TYPE_CHECKING:
    from wilde.database.entity.MonitoringEntity import MonitoringEntity


class WatcherEntity(Base):
    """
    Represents a watcher entity in the database.
    """

    __tablename__ = "watcher"

    id: Mapped[int] = mapped_column(primary_key=True)
    operation_id: Mapped[str] = mapped_column()
    plugin_id: Mapped[str] = mapped_column()

    schedule: Mapped[ScheduleEntity] = relationship(back_populates="watcher")
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedule.id"))

    monitoring: Mapped["MonitoringEntity"] = relationship(back_populates="watchers")  # One to Many
    monitoring_id: Mapped[int] = mapped_column(ForeignKey("monitoring.id"))

    def __init__(self, watcher: Watcher):
        """
        Initializes a new instance of the WatcherEntity class.

        Args:
            watcher (Watcher): The watcher object to initialize from.
        """
        super().__init__()

        self.plugin_id: str = watcher.plugin_id
        self.operation_id: str = watcher.operation.id()
        self.schedule: ScheduleEntity = ScheduleEntity(watcher.schedule)
