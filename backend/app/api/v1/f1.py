from typing import List, Optional
from typing_extensions import Annotated

from fastapi import Depends, Query, APIRouter, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.sql_models import RaceDriver, Guess, Race
from app.models.results import Standings
from app.core.dependencies import get_db, verify_token
from app.core.config import settings
from app.services.database.race_service import RaceService
from app.services.database.user_service import UserService


router = APIRouter()

DatabaseDeb = Annotated[Session, Depends(get_db)]


@router.get("/sessions", response_model=List[Race])
async def get_races(
    db: DatabaseDeb,
    limit: Optional[int] = Query(
        None, description="Number of latest races to return, or all races if omitted"
    ),
    _=Depends(verify_token),
):
    try:
        races = RaceService.get_races(db, limit)

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
async def session_drivers(
    session_id: int,
    db: DatabaseDeb,
    _=Depends(verify_token),
):
    try:
        session_drivers = RaceService.get_session_drivers(db, session_id)
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
async def user_session_guess(
    guess: Guess,
    db: DatabaseDeb,
    _=Depends(verify_token),
):
    try:
        UserService.add_guess(db, guess)
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
async def session_standing(
    db: DatabaseDeb,
    session_key: int = Query(None, description="Session key of the requested results"),
    _=Depends(verify_token),
):
    try:
        driver_numbers_in_top = RaceService.get_race_standing(db, session_key)

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

    return Standings(session_key=session_key, standings=driver_numbers_in_top)
