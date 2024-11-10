from app.services.db_service import get_database


def get_db_session():
    """Dependency to get a session with the database."""
    session = get_database().get_session()
    try:
        yield session
    finally:
        session.close()
