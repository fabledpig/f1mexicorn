from app.services.f1_api_service import F1API
from app.services.database.connector import MYSQLDB
from app.services.database.race_service import RaceService

VALID_SESSIONS = ["Qualifying", "Race"]


def initialize_sessions(mysqldb: MYSQLDB, year: str):
    sessions = F1API.get_sessions(year)

    for session in sessions:
        if session["session_type"] in VALID_SESSIONS:
            RaceService.add_race(
                mysqldb,
                session["country_name"],
                session["session_name"],
                session["date_start"],
                session["session_key"],
            )


def initialize_session_drivers(mysqldb: MYSQLDB, year: str):
    sessions = F1API.get_sessions(year)
    for session in sessions:
        if session["session_type"] in VALID_SESSIONS:
            drivers = F1API.get_session_drivers(session["session_key"])
            for driver in drivers:
                RaceService.add_session_driver(
                    mysqldb,
                    session["session_key"],
                    driver["full_name"],
                    driver["driver_number"],
                    driver["country_code"],
                    driver["team_name"],
                )


def initialize_session_results(mysqldb: MYSQLDB, year: str):
    sessions = F1API.get_sessions(year)
    for session in sessions:
        if session["session_type"] in VALID_SESSIONS:
            driver_numbers_in_top = []
            for i in range(1, 4):
                driver_numbers_in_top.append(
                    F1API.get_driver_at_position_in_session(session["session_key"], i)
                )
            RaceService.add_race_result(
                mysqldb,
                session["session_key"],
                driver_numbers_in_top[0]["driver_number"],
                driver_numbers_in_top[1]["driver_number"],
                driver_numbers_in_top[2]["driver_number"],
            )


def add_missing_sessions_in_year(mysqldb: MYSQLDB, year: str):
    sessions_database = RaceService.get_all_races(mysqldb)
    sessions_f1_api = F1API.get_sessions(year)

    session_keys_in_database = [session.race_id for session in sessions_database]
    session_keys_in_f1_api = [
        session["session_key"]
        for session in sessions_f1_api
        if session["session_type"] in VALID_SESSIONS
    ]

    missing_keys = [
        key for key in session_keys_in_f1_api if key not in session_keys_in_database
    ]
    if len(missing_keys) < 1:
        print("No sessions were added")

    for missing_key in missing_keys:
        missing_session = F1API.get_session_by_id(missing_key)
        print(missing_session)
        if missing_session["session_type"] in VALID_SESSIONS:
            RaceService.add_race(
                mysqldb,
                missing_session["country_name"],
                missing_session["session_name"],
                missing_session["date_start"],
                missing_session["session_key"],
            )
            print(f"Missing session was added by id: {missing_key}")

    # Missing session


if __name__ == "__main__":
    mysqldb = MYSQLDB()
    initialize_sessions(mysqldb, "2024")
    initialize_session_drivers(mysqldb, "2024")
    initialize_session_results(mysqldb, "2024")
    add_missing_sessions_in_year(mysqldb, "2024")
    mysqldb.close()
