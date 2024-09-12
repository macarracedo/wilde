from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from wilde.database.entity import Base
from wilde.database.entity.LocationEntity import LocationEntity
from wilde.database.entity.WatcherEntity import WatcherEntity
from wilde.scheduler.model.Monitoring import Monitoring


class MonitoringEntity(Base):
    """
    Represents a monitoring entity in the database.
    """

    __tablename__ = "monitoring"

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[LocationEntity] = relationship()
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    watchers: Mapped[List[WatcherEntity]] = relationship(back_populates="monitoring",
                                                         cascade="all, delete-orphan")  # One to Many

    def __init__(self, monitoring: Monitoring):
        """
        Initializes a new instance of the MonitoringEntity class.

        Args:
            monitoring (Monitoring): The monitoring data to initialize the entity with.
        """
        super().__init__()

        self.location: LocationEntity = LocationEntity(monitoring.location_data)
        self.watchers: list[WatcherEntity] = [WatcherEntity(watcher) for watcher in monitoring.watchers]
