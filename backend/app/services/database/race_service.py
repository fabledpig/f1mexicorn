from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Race, RaceDriver, RaceResult
from app.models.results import DriverPosition
from app.services.database.connector import MYSQLDB


class RaceService:
    """
    Queries associated with any type of F1 Session (Race, Qualification, Sprint)
    """

    @staticmethod
    def get_all_races(session: Session):
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
    def add_race_result(session: Session, race_id, first, second, third):
        try:
            query = RaceResult.race_id == race_id
            existing_result = session.exec(select(RaceResult).where(query)).first()

            if existing_result:
                # Update existing race result
                existing_result.first_place_driver_number = first
                existing_result.second_place_driver_number = second
                existing_result.third_place_driver_number = third
                session.add(existing_result)
                print("Updated existing race result")
            else:
                # Add new race result
                new_result = RaceResult(
                    race_id=race_id,
                    first_place_driver_number=first,
                    second_place_driver_number=second,
                    third_place_driver_number=third,
                )
                session.add(new_result)
                print(f"Added new race result for {race_id}")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")

    @staticmethod
    def add_session_driver(
        session: Session, session_key, driver_name, driver_number, nationality, team
    ):
        try:
            query = and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == driver_number,
            )

            existing_driver = session.exec(select(RaceDriver).where(query)).first()
            if existing_driver:
                print("Driver already added")
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
            print("Driver added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding driver:", e)

    @staticmethod
    def get_session_drivers(session: Session, session_id: int):
        try:
            sql_filter = select(RaceDriver).where(RaceDriver.race_id == session_id)
            return session.exec(sql_filter).all()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")

    @staticmethod
    def get_races(session: Session, number_of_races: int):
        try:
            sql_query = select(Race).order_by(Race.race_date.desc())

            if number_of_races and number_of_races > 0:
                sql_query = sql_query.limit(number_of_races)

            return session.exec(sql_query).all()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")

    @staticmethod
    def get_race_standing(session: Session, session_key: int):
        try:
            query_result = select(RaceResult).where(RaceResult.race_id == session_key)
            result = session.exec(query_result).first()
            print(result)
            query_drivers = []
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.first_place_driver_number,
                    )
                )
            )
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.second_place_driver_number,
                    )
                )
            )
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.third_place_driver_number,
                    )
                )
            )
            driver_numbers_in_top = []
            for pos, query in enumerate(query_drivers):
                driver_at_position = session.exec(query).first()
                print(driver_at_position)
                driver_numbers_in_top.append(
                    DriverPosition(
                        position=pos,
                        driver_number=driver_at_position.driver_number,
                        driver_name=driver_at_position.driver_name,
                    )
                )
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")
