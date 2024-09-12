from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from wilde.database.entity.LocationEntity import LocationEntity


class LocationDataDAO:
    def __init__(self, engine: Engine):
        """
        Initializes a new instance of the LocationDataDAO class.

        Args:
            engine (Engine): The database engine to be used.

        """
        self._engine: Engine = engine
        self._session_maker: sessionmaker[Session] = sessionmaker(bind=engine)

    def persist(self, location_entity: LocationEntity) -> None:
        """
        Persist a LocationData object.

        Args:
            location_entity (LocationEntity): The LocationEntity object to persist.
        """
        session: Session = self._session_maker()

        try:
            # Check if the location already exists
            existing_location = session.query(LocationEntity).filter_by(
                location=location_entity.location).one_or_none()
            
            if existing_location:
                # Location exists, append new data to the location_data list from existing location
                existing_location.add_location_data(location_entity)
                session.commit()
            else:
                # No existing location, add the new location
                session.add(location_entity)
                session.commit()
        except Exception as e:
            session.rollback()
            print("Error persisting location data:", e)
            raise
        finally:
            session.close()
