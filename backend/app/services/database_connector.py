from sqlalchemy import and_, create_engine, text
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import User, Race, RaceDriver, Guess, RaceResult
from app.core.config import settings


class MYSQLDB:
    def __init__(self) -> None:
        self._db_name = settings.database_name
        self._host = settings.host_name
        self._engine = None  # Engine will be created on startup

    def connect(self):
        """Initializes the database and creates tables if needed."""
        # Create initial connection to ensure database exists
        engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{self._host}/"
        )

        with engine.connect() as connection:
            try:
                connection.execute(
                    text(f"CREATE DATABASE IF NOT EXISTS {self._db_name}")
                )
                print(f"Database '{self._db_name}' created or already exists.")
            except SQLAlchemyError as e:
                print("Error creating database:", e)

        # Connect to the specific database
        self._engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{self._host}/{self._db_name}"
        )

        # Optionally create tables if they don't exist
        SQLModel.metadata.create_all(self._engine)

    def get_session(self):
        """Provides a session for interacting with the database."""
        if not self._engine:
            raise Exception("Database engine not initialized. Call connect() first.")
        return Session(self._engine)

    def close(self):
        """Dispose of the engine to close any active connections."""
        if self._engine:
            self._engine.dispose()
            self._engine = None

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
                query = and_(
                    RaceDriver.race_id == session_key,
                    RaceDriver.driver_number == driver_number,
                )

                existing_driver = session.exec(select(RaceDriver).where(query)).first()
                if existing_driver:
                    print("Driver already added")
                    return
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

    def add_race_result(self, race_id, first, second, third):
        with self.get_session() as session:
            try:
                query = RaceResult.race_id == race_id
                existing_result = session.exec(select(RaceResult).where(query)).first()

                if existing_result:
                    # Update existing race result
                    existing_result.first_place_driver_number = first
                    existing_result.second_place_driver_number = second
                    existing_result.third_place_driver_number = third
                    session.add(existing_result)
                    print("Updated existing race result")
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


_database_instance = None


def get_database():
    """Gets the singleton instance of MYSQLDB, initializing it if needed."""
    global _database_instance
    if _database_instance is None:
        _database_instance = MYSQLDB()
    return _database_instance
