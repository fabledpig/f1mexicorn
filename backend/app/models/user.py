from typing import Optional, Union
from pydantic import BaseModel


class GoogleAuthorizationToken(BaseModel):
    auth_token: str


class AccessToken(BaseModel):
    access_token: str


class UserInfo(BaseModel):
    email: str
    name: str
    access_token: Optional[AccessToken]
