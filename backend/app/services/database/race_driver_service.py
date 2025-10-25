
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import RaceDriver
import logging


class RaceDriverService:
    """
    Service for managing F1 Session Drivers operations.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_session_drivers(self, session: Session):
        try:
            query = select(RaceDriver)
            all_session_drivers = session.exec(query).all()
            return all_session_drivers
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error fetching all drivers: {e}")
            return []
        
    def add_session_driver(
        self, session: Session, session_key, driver_name, driver_number, nationality, team
    ):
        try:
            query = and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == driver_number,
            )

            existing_driver = session.exec(select(RaceDriver).where(query)).first()
            if existing_driver:
                self.logger.info("Driver already added")
                return
            new_driver = RaceDriver(
                race_id=session_key,
                driver_name=driver_name,
                driver_number=driver_number,
                nationality=nationality,
                team=team,
            )
            session.add(new_driver)
            session.commit()
            self.logger.info("Driver added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding driver: {e}")

    def get_session_drivers(self, session: Session, session_id: int):
        try:
            sql_filter = select(RaceDriver).where(RaceDriver.race_id == session_id)
            return session.exec(sql_filter).all()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"An error occurred: {e}")
            return []
