import requests as req

from fastapi import Depends, APIRouter, HTTPException
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


@router.post("/auth/google", response_model=UserInfo)
async def google_auth(request: AuthorizationToken):
    client_id = settings.client_id
    client_secret = settings.client_secret

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
    token_id = auth_response["id_token"]

    print(token_id)
    try:
        id_user_info = id_token.verify_oauth2_token(
            token_id, requests.Request(), client_id
        )

        user_info = UserInfo(
            user_id=id_user_info.get("sub"),
            email=id_user_info.get("email"),
            name=id_user_info.get("name"),
        )

        # TODO only add the new users to database
        database = db_service.MYSQLDB()
        database.add_user(user_info.email, user_info.name)

    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid token or verification failed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user_info
