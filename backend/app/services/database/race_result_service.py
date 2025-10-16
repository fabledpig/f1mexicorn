
from typing import List
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Guess, RaceDriver, RaceResult
from app.models.pydantic_models import DriverPosition
import logging


class RaceResultService:
    """
    Service for managing F1 Session results operations.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all_session_results(self, session: Session) -> List[RaceResult]:
        try:
            query = select(RaceResult)
            all_session_results = session.exec(query).all()
            return all_session_results
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error fetching all session results: {e}")
            return []

    def add_race_result(self, session: Session, race_id, first, second, third) -> None:
        try:
            query = RaceResult.race_id == race_id
            existing_result = session.exec(select(RaceResult).where(query)).first()

            if existing_result:
                # Update existing race result
                existing_result.position_1_driver_id = first
                existing_result.position_2_driver_id = second
                existing_result.position_3_driver_id = third
                session.add(existing_result)
                self.logger.info(f"Updated existing race result {existing_result}")
            else:
                # Add new race result
                new_result = RaceResult(
                    race_id=race_id,
                    position_1_driver_id=first,
                    position_2_driver_id=second,
                    position_3_driver_id=third,
                )
                session.add(new_result)
                self.logger.info(f"Added new race result for {race_id}")
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"An error occurred: {e}")

    def get_race_standing(self, session: Session, session_key: int) -> List[DriverPosition]:
        try:
            query_result = select(RaceResult).where(RaceResult.race_id == session_key)
            result = session.exec(query_result).first()
            
            if not result:
                self.logger.warning(f"No race result found for session {session_key}")
                return []
                
            self.logger.debug(f"Found result: {result}")
            
            query_drivers = []
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.position_1_driver_id,
                    )
                )
            )
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.position_2_driver_id,
                    )
                )
            )
            query_drivers.append(
                select(RaceDriver).where(
                    and_(
                        RaceDriver.race_id == session_key,
                        RaceDriver.driver_number == result.position_3_driver_id,
                    )
                )
            )
            
            driver_numbers_in_top = []
            for pos, query in enumerate(query_drivers):
                driver_at_position = session.exec(query).first()
                if driver_at_position:
                    self.logger.debug(f"Driver at position {pos + 1}: {driver_at_position}")
                    driver_numbers_in_top.append(
                        DriverPosition(
                            position=pos + 1,
                            driver_number=driver_at_position.race_driver_id,
                            driver_name=driver_at_position.driver_name,
                        )
                    )
                else:
                    self.logger.warning(f"No driver found at position {pos + 1} for session {session_key}")
                    
            return driver_numbers_in_top
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"An error occurred: {e}")
            return []
            
    def get_winning_guess(self, session: Session, session_id: int):
        try:
            query_session_result = select(RaceResult).where(
                RaceResult.race_id == session_id
            )
            session_result = session.exec(query_session_result).first()
            if not session_result:
                self.logger.info(f"No race result found for session_id: {session_id}")
                return None

            query_correct_guess = select(Guess).where(
                and_(
                    Guess.race_id == session_id,
                    Guess.position_1_driver_id == session_result.position_1_driver_id,
                    Guess.position_2_driver_id == session_result.position_2_driver_id,
                    Guess.position_3_driver_id == session_result.position_3_driver_id
                )
            )
            winning_guess = session.exec(query_correct_guess).first()
            if not winning_guess:
                self.logger.info(f"No winning guess found for session_id: {session_id}")
            return winning_guess
        except Exception as e:
            session.rollback()
            self.logger.error(f"An error occurred while fetching winning guess: {e}")
            return None

    