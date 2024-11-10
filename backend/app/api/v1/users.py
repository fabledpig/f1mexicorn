import jwt
import datetime
import requests as req
from fastapi import Depends, APIRouter, HTTPException, status
from sqlmodel import Session
from typing_extensions import Annotated
from google.oauth2 import id_token
from google.auth.transport import requests
from app.services import db_service
from app.models.user import AuthorizationToken, UserInfo
from app.models.sql_models import User
from app.core.dependencies import get_db_session
from app.core.config import settings

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]

GOOGLE_AUTH_URL = "https://oauth2.googleapis.com/token"

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


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
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/auth/google", response_model=UserInfo)
async def google_auth(request: AuthorizationToken):
    client_id = settings.client_id
    client_secret = settings.client_secret

    # Get the token from Google
    response = req.post(
        GOOGLE_AUTH_URL,
        data={
            "code": request.auth_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "http://localhost:3000/googlesso",
            "grant_type": "authorization_code",
        },
    )
    auth_response = response.json()
    token_id = auth_response.get("id_token")

    if not token_id:
        raise HTTPException(status_code=400, detail="Token ID not found in response")

    # Verify the Google token
    try:
        id_user_info = id_token.verify_oauth2_token(
            token_id, requests.Request(), client_id
        )

        # Create a JWT token and return it
        access_token = create_access_token(
            data={"sub": id_user_info.get("sub"), "email": id_user_info.get("email")}
        )
        user_info = UserInfo(
            user_id=id_user_info.get("sub"),
            email=id_user_info.get("email"),
            name=id_user_info.get("name"),
            access_token=access_token,
        )
        print(user_info)
    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid token or verification failed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return user_info
