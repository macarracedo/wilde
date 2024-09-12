from typing import List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from wilde.database.entity import Base
from wilde.database.entity.LocationDataEntity import LocationDataEntity
from wilde.model import LocationData


class LocationEntity(Base):
    """
    Represents a location entity in the database.
    """

    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(String(2048))
    location_data_list: Mapped[List[LocationDataEntity]] = relationship('LocationDataEntity', back_populates='location')

    __table_args__ = (UniqueConstraint("location"),)

    def __init__(self, location_data: LocationData):
        """
        Initializes a new LocationEntity object.

        Args:
            location_data (LocationData): The location data to be stored.
        """
        super().__init__()

        self.location: str = location_data.location
        self.location_data_list: list[LocationDataEntity] = [LocationDataEntity(key=dict_key, value=dict_value) for dict_key, dict_value in location_data.data.items()]
    
    def add_location_data(self, location_entity: "LocationEntity"):
        """
        Adds the location_data_list from a LocationEntity to the location_data_list.

        Args:
            location_entity (LocationEntity): The location entity from which data will be added.
        """
        for ld_entity in location_entity.location_data_list:
            self.location_data_list.append(LocationDataEntity(key=ld_entity.key, value=ld_entity.value))