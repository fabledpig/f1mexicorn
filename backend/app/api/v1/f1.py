import logging
from typing import List, Optional
from sqlmodel import Session
from typing_extensions import Annotated

from fastapi import Depends, Query, APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.models.sql_models import RaceDriver, Race, Guess
from app.models.pydantic_models import Standings
from app.core.dependencies import get_db_session, verify_token
from app.core.config import settings
from app.services.database.race_service import RaceService
from app.services.database.user_service import UserService
from app.services.database.race_driver_service import RaceDriverService
from app.services.database.race_result_service import RaceResultService

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/sessions", response_model=List[Race])
async def get_races(
    session: SessionDep,
    limit: int = Query(
        0, description="Number of latest races to return, or all races if omitted"
    ),
    _=Depends(verify_token),
):
    try:
        races = RaceService.get_races(session, limit)

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
@router.get("/session_drivers", response_model=List[RaceDriver])
async def session_drivers(
    session_id: int,
    session: SessionDep,
    _=Depends(verify_token),
):
    try:
        session_drivers = RaceDriverService.get_session_drivers(session, session_id)
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


@router.post("/guess", response_model=Guess)
async def user_session_guess(
    guess: Guess,
    session: SessionDep,
):
    try:
        UserService.add_guess(session, guess)
        return guess

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )

    except Exception as e:
        logging.error(f"Error occurred while adding guess: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {str(e)}",
        )


# TODO how to do this, always fetch from F1 openapi,
# or cache some and only request at regular intervals, probably need to use redis here
@router.get("/session_standing", response_model=Standings)
async def session_standing(
    session: SessionDep,
    session_key: int = Query(None, description="Session key of the requested results"),
    _=Depends(verify_token),
):
    try:
        driver_numbers_in_top = RaceResultService.get_race_standing(session, session_key)

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
    print(driver_numbers_in_top)
    return Standings(session_key=session_key, standings=driver_numbers_in_top)
