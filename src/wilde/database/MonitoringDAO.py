from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from wilde.database.entity.MonitoringEntity import MonitoringEntity
from wilde.database.entity.LocationEntity import LocationEntity


class MonitoringDAO:
    def __init__(self, engine: Engine):
        """
        Initializes a new instance of the MonitoringDAO class.

        Args:
            engine (Engine): The database engine to be used.

        """
        self._engine: Engine = engine
        self._session_maker: sessionmaker[Session] = sessionmaker(bind=engine)

    def persist(self, monitoring: MonitoringEntity) -> None:
        """
        Persist a MonitoringEntity object.

        Args:
            monitoring (MonitoringEntity): The MonitoringEntity object to persist.
        """
        session: Session = self._session_maker()
        try:
            # Attempt to find an existing location by the unique location attribute
            existing_location = session.query(LocationEntity).filter_by(
                location=monitoring.location.location).one_or_none()

            if existing_location:
                # If location exists, reuse the existing location entity
                monitoring.location = existing_location
            
            # Add the new monitoring data. This will also add the location, or link to the existing location
            session.add(monitoring)
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error persisting monitoring data:", e)
            raise
        finally:
            session.close()
