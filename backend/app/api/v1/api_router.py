from fastapi import APIRouter
from app.api.v1 import users, f1_data

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(f1_data.router, prefix="/f1", tags=["f1"])
