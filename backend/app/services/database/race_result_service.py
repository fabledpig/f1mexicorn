
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Race, RaceDriver, RaceResult
from app.models.results import DriverPosition


class RaceResultService:
    """
    Queries associated with F1 Session results
    """

    @staticmethod
    def get_all_session_results(session: Session):
        try:
            query = select(RaceResult)
            all_session_results = session.exec(query).all()
            return all_session_results
        except SQLAlchemyError as e:
            session.rollback()
            print("Error fetchin all drivers:", e)    
    

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
                print(f"Updated existing race result {existing_result}")
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
