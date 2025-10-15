from sqlmodel import Session
from typing_extensions import Annotated
import requests as req
from fastapi import Depends, APIRouter, HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests
from app.models.user import GoogleAuthorizationToken, AccessToken, UserInfo
from app.core.dependencies import create_access_token, get_db_session, verify_token
from app.core.config import settings
from app.services.database.user_service import UserService

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


@router.post("/auth/google", response_model=UserInfo)
async def google_auth(
    request: GoogleAuthorizationToken,
    db: SessionDep,
) -> UserInfo:
    client_id = settings.client_id
    try:
        id_user_info = id_token.verify_oauth2_token(
            request.auth_token, requests.Request(), client_id, 10
        )
        # Create a JWT token and return it
        access_token = create_access_token(
            data={"name": id_user_info.get("name"), "email": id_user_info.get("email")}
        )
        print(access_token)

        # Add to db the existing user (will only add if new)
        UserService.add_user(db, id_user_info.get("name"), id_user_info.get("email"))

        return UserInfo(
            name=id_user_info.get("name"),
            email=id_user_info.get("email"),
            access_token=AccessToken(access_token=access_token),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user", response_model=UserInfo)
async def get_user_info(
    decoded_token=Depends(verify_token),
):
    return decoded_token
