import mysql.connector
from app.utils.utils import get_database_credentials
import mysql.connector
from mysql.connector import Error


class MYSQLDB:
    def __init__(self, db_name="f1_application", host="localhost") -> None:
        self._database_name = db_name
        try:
            self._connection = mysql.connector.connect(
                host=host,
                database=db_name,
                user=get_database_credentials()[0],
                password=get_database_credentials()[1],
            )
            self._cursor = self._connection.cursor()
        except Error as e:
            print("Error connecting to MYSQL:", e)
            return None

    def __del__(self):
        if self._connection.is_connected():
            self._connection.close()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    def add_user(self, username, email):
        try:
            add_user_query = """
            INSERT INTO users (username, email) VALUES (%s, %s)
            """
            self._cursor.execute(add_user_query, (username, email))
            self._connection.commit()
            print("User added successfully")
        except Error as e:
            print("Error adding user:", e)

    def add_driver(self, driver_name, nationality, team):
        try:
            add_driver_query = """
            INSERT INTO drivers (driver_name, nationality, team) VALUES (%s,%s,%s)
            """
            self._cursor.execute(add_driver_query, (driver_name, nationality, team))
            self._connection.commit()
        except Error as e:
            print("error adding driver:", e)

    def add_race(self, race_name, race_date):
        try:
            add_race_query = """
            INSERT INTO races (race_name, race_date) VALUES (%s, %s)
            """
            self._cursor.execute(add_race_query, (race_name, race_date))
            self._connection.commit()
            print("Race added successfully")
        except Error as e:
            print("Error adding race:", e)

    def add_race_result(self, race_id, driver_id, position):
        try:
            add_result_query = """
            INSERT INTO race_results (race_id, driver_id, position) VALUES (%s, %s, %s)
            """
            self._cursor.execute(add_result_query, (race_id, driver_id, position))
            self._connection.commit()
            print("Race result added successfully")
        except Error as e:
            print("Error adding race result:", e)

    def add_guess(
        self,
        user_id,
        race_id,
        position_1_driver_id,
        position_2_driver_id,
        position_3_driver_id,
    ):
        try:
            add_guess_query = """
            INSERT INTO guesses (user_id, race_id, position_1_driver_id, position_2_driver_id, position_3_driver_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            self._cursor.execute(
                add_guess_query,
                (
                    user_id,
                    race_id,
                    position_1_driver_id,
                    position_2_driver_id,
                    position_3_driver_id,
                ),
            )
            self._connection.commit()
            print("Guess added successfully")
        except Error as e:
            print("Error adding guess:", e)
