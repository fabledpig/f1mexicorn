from pydantic import BaseModel


class GoogleAuthorizationToken(BaseModel):
    auth_token: str


class AccessToken(BaseModel):
    access_token: str


class UserInfo(BaseModel):
    email: str
    name: str
