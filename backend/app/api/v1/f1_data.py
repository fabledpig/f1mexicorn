from datetime import datetime
from typing import List
from typing_extensions import Annotated

from fastapi import Depends, APIRouter
from sqlmodel import Session, select

from app.models.sql_models import RaceDriver, Guess, Race
from app.services.db_service import MYSQLDB

from app.services.f1_api_service import F1API

router = APIRouter()

mysqldb = MYSQLDB()

SessionDep = Annotated[Session, Depends(mysqldb.get_session)]


# Provide all guessable sessions past and future
@router.get("/races", response_model=List[Race])
async def sessions(session: SessionDep):
    races = session.exec(select(Race)).all()
    return races


# Provide latest session which can still be guessed
@router.get("/latest_race")
async def latest_session(session: SessionDep):
    # Current date and time to filter future races
    # now = datetime.now()
    sql_filter = select(Race).order_by(Race.race_date.desc()).limit(1)
    latest_race = session.exec(sql_filter).first()
    return latest_race


# Provide
@router.post("/session_drivers", response_model=List[RaceDriver])
async def session_drivers(session_id: int, session: SessionDep):
    print(session_id)
    sql_filter = select(RaceDriver).where(RaceDriver.race_id == session_id)
    session_drivers = session.exec(sql_filter).all()

    return session_drivers


@router.post("/guess")
async def user_session_guess(guess: Guess, session: SessionDep):
    pass
