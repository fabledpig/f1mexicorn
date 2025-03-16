from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
import app.models.sql_models

class MYSQLDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MYSQLDB, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._db_name = settings.database_name
        self._host = settings.host_name
        self._engine = None

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
