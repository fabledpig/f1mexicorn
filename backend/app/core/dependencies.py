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

ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = HTTPBearer()


def verify_token(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
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


def get_db_session(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.db.get_session()
    try:
        yield session
    finally:
        session.close()
