from typing import Optional
from typing import TYPE_CHECKING

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from wilde.database.entity import Base
from wilde.scheduler.model.Schedule import Schedule

if TYPE_CHECKING:
    from wilde.database.entity.WatcherEntity import WatcherEntity


class ScheduleEntity(Base):
    """
    Represents a schedule entity in the database.
    """

    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(primary_key=True)
    interval: Mapped[int] = mapped_column(Integer)
    start: Mapped[Optional[int]] = mapped_column(Integer)  # Nullable implicit
    watcher: Mapped["WatcherEntity"] = relationship(back_populates="schedule")

    def __init__(self, schedule: Schedule):
        """
        Initializes a new instance of the ScheduleEntity class.

        Args:
            schedule (Schedule): The schedule object containing the data.
        """
        super().__init__()

        self.interval: int = schedule.interval
        self.start: int = schedule.start
