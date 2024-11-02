from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.utils.utils import get_database_credentials

from app.models.sql_models import (
    Base,
    User,
    Driver,
    Race,
    RaceDriver,
    RaceResult,
    Guess,
)


class MYSQLDB:
    def __init__(self, db_name="f1_application", host="localhost") -> None:
        self._db_name = db_name
        self._engine = create_engine(
            f"mysql+mysqlconnector://{get_database_credentials()[0]}:{get_database_credentials()[1]}@{host}/"
        )

        # Create the Database initially, might not be the best, but for now
        with self._engine.connect() as connection:
            try:
                connection.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {self._db_name}")
                )
                print(f"Database '{self._db_name}' created or already exists.")
            except SQLAlchemyError as e:
                print("Error creating database:", e)

        # Connect to the created db
        self._engine = create_engine(
            f"mysql+mysqlconnector://{get_database_credentials()[0]}:{get_database_credentials()[1]}@{host}/{self._db_name}"
        )
        self._session = sessionmaker(bind=self._engine)

    @property
    def session(self):
        """Provides a new session to interact with the database."""
        return self._session()

    def create_tables(self):
        """Create tables in the database if they do not exist."""
        try:
            Base.metadata.create_all(self._engine)
            print("Tables created successfully.")
        except SQLAlchemyError as e:
            print("Error creating tables:", e)

    def get_all_races(self):
        """Fetch all records from the races table."""
        with self._session() as session:
            try:
                races = session.query(Race).all()  # Query to get all races
                return races
            except SQLAlchemyError as e:
                print("Error fetching races:", e)
                return []

    def add_user(self, username, email):
        session = self._session()
        try:
            new_user = User(username=username, email=email)
            session.add(new_user)
            session.commit()
            print("User added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding user:", e)
        finally:
            session.close()

    def add_driver(self, driver_name, nationality, team):
        session = self._session()
        try:
            existing_driver = (
                session.query(Driver)
                .filter_by(driver_name=driver_name, nationality=nationality)
                .first()
            )
            if existing_driver:
                print(f"Driver '{driver_name}' already exists.")
                return
            new_driver = Driver(
                driver_name=driver_name, nationality=nationality, team=team
            )
            session.add(new_driver)
            session.commit()
            print("Driver added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding driver:", e)
        finally:
            session.close()

    def add_race(self, race_name, race_type, race_date, race_id=None):
        session = self._session()
        try:
            existing_race = (
                session.query(Race)
                .filter_by(race_name=race_name, race_type=race_type)
                .first()
            )
            if existing_race:
                print(f"Race '{race_name}'_'{race_type}' already exists.")
                return
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
        finally:
            session.close()

    def add_race_result(self, race_id, driver_id, position):
        session = self._session()
        try:
            new_result = RaceResult(
                race_id=race_id, driver_id=driver_id, position=position
            )
            session.add(new_result)
            session.commit()
            print("Race result added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding race result:", e)
        finally:
            session.close()

    def add_guess(
        self,
        user_id,
        race_id,
        position_1_driver_id,
        position_2_driver_id,
        position_3_driver_id,
    ):
        session = self._session()
        try:
            new_guess = Guess(
                user_id=user_id,
                race_id=race_id,
                position_1_driver_id=position_1_driver_id,
                position_2_driver_id=position_2_driver_id,
                position_3_driver_id=position_3_driver_id,
            )
            session.add(new_guess)
            session.commit()
            print("Guess added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding guess:", e)
        finally:
            session.close()
