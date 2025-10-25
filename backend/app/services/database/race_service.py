from typing import List
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Race
import logging

class RaceService:
    """
    Service for managing F1 Sessions (Race, Qualification, Sprint) operations.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_races(self, session: Session) -> List[Race]:
        """Fetch all records from the races table."""
        try:
            races = session.exec(select(Race)).all()
            return races
        except SQLAlchemyError as e:
            self.logger.error(f"Error fetching races: {e}")
            return []

    def add_race(self, session: Session, race_name, race_type, race_date, race_id=None):
        try:
            new_race = Race(
                race_id=race_id,
                race_name=race_name,
                race_type=race_type,
                race_date=race_date,
            )
            session.add(new_race)
            session.commit()
            self.logger.info("Race added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding race: {e}")

    def get_races(self, session: Session, number_of_races: int = 0) -> List[Race]:
        try:
            sql_query = select(Race).order_by(Race.race_date.desc())

            if number_of_races > 0:
                sql_query = sql_query.limit(number_of_races)

            return session.exec(sql_query).all()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"An error occurred: {e}")
            return []