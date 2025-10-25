import logging
from typing import List, Optional
from dataclasses import dataclass, field

from sqlmodel import Session
from app.services.f1openapi.f1_api_service import F1API
from sqlalchemy.exc import SQLAlchemyError
from app.services.database.race_service import RaceService
from app.services.database.race_driver_service import RaceDriverService
from app.services.database.race_result_service import RaceResultService
from app.services.database.connector import get_db_manager

logging.basicConfig(level=logging.INFO)

@dataclass
class SyncResult:
    """Result of a database synchronization operation."""
    added_sessions: int = 0
    added_drivers: int = 0
    added_results: int = 0
    errors: List[str] = field(default_factory=list)

class DatabaseService:
    """Service for synchronizing F1 data between API and database."""
    
    def __init__(self, f1_api: Optional[F1API] = None):
        self.f1_api = f1_api or F1API()
        self.race_service = RaceService()
        self.driver_service = RaceDriverService()
        self.result_service = RaceResultService()
        self.valid_sessions = ["Qualifying", "Race"]
        self.logger = logging.getLogger(__name__)

    def set_valid_sessions(self, valid_sessions_list: List[str]) -> None:
        """Set which session types to sync."""
        self.valid_sessions = valid_sessions_list

    def sync_year_data(self, year: str) -> SyncResult:
        """Sync all data for a given year."""
        result = SyncResult()
        
        with get_db_manager().get_session_context() as session:
            try:
                # Sync sessions first
                session_result = self.add_missing_sessions_in_year(session, year)
                result.added_sessions = session_result
                
                # Sync drivers
                driver_result = self.add_missing_session_drivers(session)
                result.added_drivers = driver_result
                
                # Sync results
                results_result = self.add_missing_session_results(session)
                result.added_results = results_result
                
                self.logger.info(f"Sync completed: {result}")
                return result
                
            except Exception as e:
                result.errors.append(str(e))
                self.logger.error(f"Sync failed: {e}")
                raise

    def add_missing_sessions_in_year(self, session: Session, year: str) -> int:
        """
        Adds missing sessions in a year to the database.
        Args:
            session: The database session
            year: The year for which to add missing sessions
        Returns:
            Number of sessions added
        """
        added_count = 0
        try:
            sessions_database = self.race_service.get_all_races(session)
            sessions_f1_api = self.f1_api.get_sessions(year)

            session_keys_in_database = {session_obj.race_id for session_obj in sessions_database}
            session_keys_in_f1_api = {
                session_data["session_key"]
                for session_data in sessions_f1_api
                if session_data["session_type"] in self.valid_sessions
            }

            missing_keys = session_keys_in_f1_api - session_keys_in_database
            if not missing_keys:
                self.logger.info("No missing sessions found.")
                return added_count

            missing_sessions = [
                self.f1_api.get_session_by_id(missing_key) for missing_key in missing_keys
            ]

            # Filter again in case API returns unexpected types
            valid_sessions = [
                s 
                for session_list in missing_sessions
                for s in session_list
                if s["session_type"] in self.valid_sessions
            ]

            # Batch insert
            for session_data in valid_sessions:
                self.race_service.add_race(
                    session,
                    session_data["country_name"],
                    session_data["session_name"],
                    session_data["date_start"],
                    session_data["session_key"],
                )
                added_count += 1
                self.logger.info(f"Added missing session with ID: {session_data['session_key']}")

            self.logger.info(f"Added {added_count} missing sessions.")
            return added_count
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding session: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise
            
    def add_missing_session_drivers(self, session: Session) -> int:
        """
        Adds missing session drivers to the database.
        Args:
            session: The database session
        Returns:
            Number of drivers added
        """
        added_count = 0
        try:
            all_f1_sessions = self.race_service.get_all_races(session)
            all_f1_session_drivers = self.driver_service.get_all_session_drivers(session)
            
            # Compare which sessions have no drivers in db
            session_keys_without_drivers = set([race.race_id for race in all_f1_sessions]) - set([driver.race_id for driver in all_f1_session_drivers])
            
            for missing_session_key in session_keys_without_drivers:
                drivers = self.f1_api.get_session_drivers(missing_session_key)
                for driver in drivers:
                    self.driver_service.add_session_driver(
                        session,
                        missing_session_key,
                        driver["full_name"],
                        driver["driver_number"],
                        driver["country_code"],
                        driver["team_name"],
                    )
                    added_count += 1
                    
            self.logger.info(f"Added {added_count} missing drivers.")
            return added_count
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding driver: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise

    def add_missing_session_results(self, session: Session) -> int:
        """
        Adds missing session results to the database.
        Args:
            session: The database session
        Returns:
            Number of results added
        """
        added_count = 0
        try:
            all_f1_sessions = self.race_service.get_all_races(session)
            all_f1_session_results = self.result_service.get_all_session_results(session)
            
            # Compare which sessions have no results in db
            session_keys_without_results = set([race.race_id for race in all_f1_sessions]) - set([result.race_id for result in all_f1_session_results])
            
            self.logger.info(f"Session keys without results: {session_keys_without_results}")
            
            for session_key in session_keys_without_results:
                driver_numbers_in_top = []
                for i in range(1, 4):
                    driver_numbers_in_top.append(
                        self.f1_api.get_driver_at_position_in_session(session_key, i)
                    )
                    
                self.logger.debug(f"Top 3 drivers for session {session_key}: {driver_numbers_in_top}")
                
                self.result_service.add_race_result(
                    session,
                    session_key,
                    driver_numbers_in_top[0]["driver_number"],
                    driver_numbers_in_top[1]["driver_number"],
                    driver_numbers_in_top[2]["driver_number"],
                )
                added_count += 1

            self.logger.info(f"Added {added_count} missing results.")
            return added_count

        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Error adding session result: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise

    def update_latest_session_results(self, session: Session) -> int:
        """
        Updates the latest session results.
        Args:
            session: The database session
        Returns:
            Number of results updated
        """
        # TODO: Implement periodic update logic
        self.logger.info("Update latest session results - not yet implemented")
        return 0
    