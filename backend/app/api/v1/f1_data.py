from datetime import datetime
from typing import List, Optional
from typing_extensions import Annotated

from fastapi import Depends, Query, APIRouter, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from app.services.f1_api_service import F1API
from app.models.sql_models import RaceDriver, Guess, Race
from app.models.results import DriverPosition, Standings
from app.core.dependencies import get_db_session

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/sessions", response_model=List[Race])
async def get_races(
    session: SessionDep,
    limit: Optional[int] = Query(
        None, description="Number of latest races to return, or all races if omitted"
    ),
):
    try:
        sql_query = select(Race).order_by(Race.race_date.desc())

        if limit and limit > 0:
            sql_query = sql_query.limit(limit)

        races = session.exec(sql_query).all()

        if not races:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No races found"
            )

        return races

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# Provide
@router.post("/session_drivers", response_model=List[RaceDriver])
async def session_drivers(session_id: int, session: SessionDep):
    try:
        sql_filter = select(RaceDriver).where(RaceDriver.race_id == session_id)
        session_drivers = session.exec(sql_filter).all()

        if not session_drivers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No drivers found for session with ID {session_id}",
            )

        return session_drivers

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {str(e)}",
        )


@router.post("/guess")
async def user_session_guess(guess: Guess, session: SessionDep):
    try:
        session.add(guess)
        session.commit()
        session.refresh(guess)
        return {"message": "Guess added successfully", "guess_id": guess.id}

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# TODO how to do this, always fetch from F1 openapi,
# or cache some and only request at regular intervals, probably need to use redis here
@router.post("/session_standing", response_model=Standings)
async def session_standing(session_key: int):
    driver_numbers_in_top = []
    for i in range(1, 4):
        driver_at_position = F1API.get_driver_at_position_in_session(session_key, i)
        driver_numbers_in_top.append(
            DriverPosition(
                position=i, driver_number=driver_at_position["driver_number"]
            )
        )
    return Standings(session_key=session_key, standings=driver_numbers_in_top)
