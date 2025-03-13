from typing import List
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Race

class RaceService:
    """
    Queries associated with any type of F1 Session (Race, Qualification, Sprint)
    """

    @staticmethod
    def get_all_races(session: Session) -> List[Race]:
        """Fetch all records from the races table."""
        try:
            races = session.exec(select(Race)).all()
            return races
        except SQLAlchemyError as e:
            print("Error fetching races:", e)
            return []

    @staticmethod
    def add_race(session: Session, race_name, race_type, race_date, race_id=None):
        try:
            new_race = Race(
                race_id=race_id,
                race_name=race_name,
                race_type=race_type,
                race_date=race_date,
            )
            session.add(new_race)
            session.commit()
            print("Race added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding race:", e)

    @staticmethod
    def get_races(session: Session, number_of_races: int = 0) -> List[Race]:
        try:
            sql_query = select(Race).order_by(Race.race_date.desc())

            if number_of_races > 0:
                sql_query = sql_query.limit(number_of_races)

            return session.exec(sql_query).all()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")