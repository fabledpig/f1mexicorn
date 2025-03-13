import logging
from typing import List

from sqlmodel import Session
from app.services.f1openapi.f1_api_service import F1API
from sqlalchemy.exc import SQLAlchemyError
from app.services.database.race_service import RaceService
from app.services.database.race_driver_service import RaceDriverService
from app.services.database.race_result_service import RaceResultService

logging.basicConfig(level=logging.INFO)

class DatabaseService:
    VALID_SESSIONS = ["Qualifying", "Race"]

    @staticmethod
    def set_valid_sessions(valid_sessions_list: List[str]) -> None:
        DatabaseService.VALID_SESSIONS = valid_sessions_list

    @staticmethod
    def add_missing_sessions_in_year(database_session: Session, year: str) -> None:
        try:
            """Fetches all sessions from the API and database, adds missing ones."""
            sessions_database = RaceService.get_all_races(database_session)
            sessions_f1_api = F1API.get_sessions(year)

            session_keys_in_database = {session.race_id for session in sessions_database}
            session_keys_in_f1_api = {
                session["session_key"]
                for session in sessions_f1_api
                if session["session_type"] in DatabaseService.VALID_SESSIONS
            }

            missing_keys = session_keys_in_f1_api - session_keys_in_database
            if not missing_keys:
                logging.info("No missing sessions found.")
                return

            missing_sessions = [
                F1API.get_session_by_id(missing_key) for missing_key in missing_keys
            ]

            # Filter again in case API returns unexpected types
            valid_sessions = [
                s 
                for session_list in missing_sessions
                for s in session_list
                if s["session_type"] in DatabaseService.VALID_SESSIONS
            ]

            # Batch insert
            for session in valid_sessions:
                RaceService.add_race(
                    database_session,
                    session["country_name"],
                    session["session_name"],
                    session["date_start"],
                    session["session_key"],
                )
                logging.info(f"Added missing session with ID: {session['session_key']}")

            logging.info("All missing sessions have been added.")
        except SQLAlchemyError as e:
            database_session.rollback()
            print("Error adding session:", e)
        except Exception as e:
            print("Error:", e)
            
    @staticmethod
    def add_missing_session_drivers(database_session: Session):
        try:
            all_f1_sessions = RaceService.get_all_races(database_session)
            all_f1_session_drivers = RaceDriverService.get_all_session_drivers(database_session)
            
            # compare which sessions has no drivers in db
            session_keys_without_drivers = set([race.race_id for race in all_f1_sessions]) - set([driver.race_id for driver in all_f1_session_drivers])
            
            for missing_session_key in session_keys_without_drivers:
                drivers = F1API.get_session_drivers(missing_session_key)
                for driver in drivers:
                    RaceDriverService.add_session_driver(
                        database_session,
                        missing_session_key,
                        driver["full_name"],
                        driver["driver_number"],
                        driver["country_code"],
                        driver["team_name"],
                    )
        except SQLAlchemyError as e:
            database_session.rollback()
            print("Error adding driver:", e)
        except Exception as e:
            print("Error:", e)


    @staticmethod
    def add_missing_session_results(database_session: Session):
        try:
            all_f1_sessions = RaceService.get_all_races(database_session)
            all_f1_session_results = RaceResultService.get_all_session_results(database_session)
            
            # compare which sessions has no drivers in db
            session_keys_without_results = set([race.race_id for race in all_f1_sessions]) - set([driver.race_id for driver in all_f1_session_results])
            
            for session_key in session_keys_without_results:
                driver_numbers_in_top = []
                for i in range(1, 4):
                    driver_numbers_in_top.append(
                        F1API.get_driver_at_position_in_session(session_key, i)
                    )
                RaceResultService.add_race_result(
                    database_session,
                    session_key,
                    driver_numbers_in_top[0]["driver_number"],
                    driver_numbers_in_top[1]["driver_number"],
                    driver_numbers_in_top[2]["driver_number"],
                )

        except SQLAlchemyError as e:
            database_session.rollback()
            print("Error adding session result:", e)
        except Exception as e:
            print("Error:", e)
