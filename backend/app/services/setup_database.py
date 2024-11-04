from app.services.f1_api_service import F1API
from app.services.db_service import MYSQLDB


def populate_races(f1api: F1API, mysqldb: MYSQLDB):
    sessions = f1api.get_sessions()
    valid_sessions = ["Qualifying", "Race"]
    for session in sessions:
        if session["session_type"] in valid_sessions:
            mysqldb.add_race(
                session["country_name"],
                session["session_name"],
                session["date_start"],
                session["session_key"],
            )


def populate_drivers(f1api: F1API, mysqldb: MYSQLDB):
    meetings = f1api.get_meetings()
    for meeting in meetings:
        drivers = f1api.get_drivers(meeting["meeting_key"])
        for driver in drivers:
            mysqldb.add_driver(
                driver["full_name"], driver["country_code"], driver["team_name"]
            )


if __name__ == "__main__":
    f1api = F1API(2024)
    mysqldb = MYSQLDB()

    mysqldb.create_tables()
    populate_races(f1api, mysqldb)
    populate_drivers(f1api, mysqldb)
