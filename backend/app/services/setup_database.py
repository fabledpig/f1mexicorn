from app.services.f1_api_service import F1API
from app.services.db_service import MYSQLDB

VALID_SESSIONS = ["Qualifying", "Race"]


def populate_races(mysqldb: MYSQLDB):
    sessions = F1API.get_sessions("2024")

    for session in sessions:
        if session["session_type"] in VALID_SESSIONS:
            mysqldb.add_race(
                session["country_name"],
                session["session_name"],
                session["date_start"],
                session["session_key"],
            )


def populate_session_drivers(mysqldb: MYSQLDB):
    sessions = F1API.get_sessions("2024")
    for session in sessions:
        if session["session_type"] in VALID_SESSIONS:
            drivers = F1API.get_session_drivers(session["session_key"])
            for driver in drivers:
                mysqldb.add_session_driver(
                    session["session_key"],
                    driver["full_name"],
                    driver["driver_number"],
                    driver["country_code"],
                    driver["team_name"],
                )


if __name__ == "__main__":
    mysqldb = MYSQLDB()
    mysqldb.connect()
    populate_races(mysqldb)
    populate_session_drivers(mysqldb)
    mysqldb.close()
