from fastapi import APIRouter
from app.models.sql_models import Guess

router = APIRouter()


@router.get("/sessions")
async def sessions():
    pass


@router.get("/latest_session")
async def latest_session():
    pass


@router.get("/all_drivers")
async def all_drivers():
    pass


@router.post("/session_drivers")
async def session_drivers():
    pass


@router.post("/guess")
async def user_session_guess(guess: Guess):
    pass
