from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from wilde.database.entity import Base
if TYPE_CHECKING:
    from wilde.database.entity.LocationEntity import LocationEntity


class LocationDataEntity(Base):
    """
    Represents a location data entity.

    Attributes:
        location_id (int): The ID of the associated location.
        timestamp (datetime): The timestamp of the location data.
        key (str): The key associated with the location data.
        value (str): The value associated with the location data.
        location (LocationEntity): The associated location entity.
    """

    __tablename__ = 'location_data'

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()

    location: Mapped["LocationEntity"] = relationship(back_populates="location_data_list")

    def __init__(self, key: str, value: str):
        """
        Initializes a new instance of the LocationDataEntity class.

        Args:
            key (str): The key associated with the location data.
            value (str): The value associated with the location data.
        """
        super().__init__()

        self.timestamp: datetime = datetime.now()
        self.key: str = key
        self.value: str = value
