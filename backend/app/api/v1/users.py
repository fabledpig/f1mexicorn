from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req
import json

from app.utils.utils import get_google_auth_client_credentials

router = APIRouter()

GOOGLE_AUTH_URL = "https://oauth2.googleapis.com/token"


class AuthorizationToken(BaseModel):
    auth_token: str


class UserInfo(BaseModel):
    user_id: str
    email: str
    name: str


@router.post("/auth/google", response_model=UserInfo)
async def google_auth(request: AuthorizationToken):
    client_id, client_secret = get_google_auth_client_credentials()

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

    except ValueError:
        raise HTTPException(
            status_code=401, detail="Invalid token or verification failed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return user_info


@router.get("/users/", tags=["users"])
async def read_users():
    # from Google SSO data
    return [
        {"user_id": 1, "name": "Alice"},
    ]


@router.post("/users/", tags=["users"])
async def create_user(name: str):
    return {"user_id": 3, "name": name}
