from fastapi import APIRouter
from app.api.v1 import users, f1, results

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users")
api_router.include_router(f1.router, prefix="/f1")
api_router.include_router(results.router, prefix="/results")
