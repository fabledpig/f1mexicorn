from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from contextlib import contextmanager
from sqlalchemy.pool import QueuePool
from functools import lru_cache

class DatabaseManager:
    def __init__(self):
        self._db_name = settings.database_name
        self._host = settings.host_name
        self._engine = None
        self._session_factory = None
        
        self._initialize_database()

    def _initialize_database(self):
        """Initialize database and create tables if needed."""
        # First, create database if it doesn't exist
        temp_engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{self._host}/",
            echo=False
        )

        with temp_engine.connect() as connection:
            try:
                connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {self._db_name}"))
                connection.commit()
                print(f"Database '{self._db_name}' ready.")
            except SQLAlchemyError as e:
                print(f"Error creating database: {e}")
                raise
        
        temp_engine.dispose()

        # Create main engine with connection pooling
        self._engine = create_engine(
            f"mysql+mysqlconnector://{settings.mysql_user}:{settings.mysql_password}@{self._host}/{self._db_name}",
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )

        # Create session factory
        from sqlalchemy.orm import sessionmaker
        self._session_factory = sessionmaker(bind=self._engine)

        # Create tables
        SQLModel.metadata.create_all(self._engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        if not self._session_factory:
            raise RuntimeError("Database not initialized")
        return Session(self._engine)

    @contextmanager
    def get_session_context(self):
        """Context manager for database sessions with automatic cleanup."""
        session = self.get_session()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def close(self):
        """Close all connections and dispose engine."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    def reset(self):
        """Reset the manager (mainly for testing)."""
        self.close()

@lru_cache(maxsize=1)
def get_db_manager() -> DatabaseManager:
    """Get the singleton database manager instance."""
    return DatabaseManager()