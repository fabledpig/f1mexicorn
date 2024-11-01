from pydantic import BaseModel


class AuthorizationToken(BaseModel):
    auth_token: str


class UserInfo(BaseModel):
    user_id: str
    email: str
    name: str
