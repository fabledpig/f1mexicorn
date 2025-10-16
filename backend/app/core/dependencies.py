from typing import Generator
import jwt
import datetime
from fastapi import Depends, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlmodel import Session
from app.core.config import settings
from app.services.database.connector import get_db_manager


from app.core.container import (
    get_f1_api,
    get_database_service, 
    get_race_service,
    get_race_driver_service,
    get_race_result_service,
    get_user_service
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = HTTPBearer()


def verify_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token.credentials, settings.secret_key, algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def create_access_token(data: dict, expires_delta: datetime.timedelta = None):
    """Generate JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    # Directly pass the dictionary to jwt.encode without encoding it to bytes
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.
    Uses the new singleton database manager.
    """
    with get_db_manager().get_session_context() as session:
        yield session
