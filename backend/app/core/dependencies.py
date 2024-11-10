from fastapi.security import OAuth2PasswordBearer
from app.services.db_service import get_database


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db_session():
    """Dependency to get a session with the database."""
    session = get_database().get_session()
    try:
        yield session
    finally:
        session.close()
