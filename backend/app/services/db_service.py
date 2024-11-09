from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import User, Race, RaceDriver, RaceResult, Guess
from app.core.config import settings


class MYSQLDB:
    def __init__(self, db_name="f1_application", host="localhost") -> None:
        self._db_name = db_name
        self._engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{host}/"
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

        # Connect to the created database
        self._engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{host}/{self._db_name}"
        )

    def create_tables(self):
        """Create tables in the database if they do not exist."""
        try:
            SQLModel.metadata.create_all(self._engine)
            print("Tables created successfully.")
        except SQLAlchemyError as e:
            print("Error creating tables:", e)

    def get_session(self):
        """Provides a new session to interact with the database."""
        return Session(self._engine)

    def get_all_races(self):
        """Fetch all records from the races table."""
        with self.get_session() as session:
            try:
                races = session.exec(select(Race)).all()
                return races
            except SQLAlchemyError as e:
                print("Error fetching races:", e)
                return []

    def add_user(self, username, email):
        with self.get_session() as session:
            try:
                new_user = User(username=username, email=email)
                session.add(new_user)
                session.commit()
                print("User added successfully")
            except SQLAlchemyError as e:
                session.rollback()
                print("Error adding user:", e)

    def add_session_driver(
        self, session_key, driver_name, driver_number, nationality, team
    ):
        with self.get_session() as session:
            try:
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

    def add_race(self, race_name, race_type, race_date, race_id=None):
        with self.get_session() as session:
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

    def add_race_result(self, race_id, driver_id, position):
        with self.get_session() as session:
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

    def add_guess(
        self,
        user_id,
        race_id,
        position_1_driver_id,
        position_2_driver_id,
        position_3_driver_id,
    ):
        with self.get_session() as session:
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
