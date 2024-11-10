from datetime import datetime
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing_extensions import Annotated

from fastapi import Depends, Query, APIRouter, HTTPException, status
from sqlmodel import Session, and_, select
from sqlalchemy.exc import SQLAlchemyError

from app.services.f1_api_service import F1API
from app.models.sql_models import RaceDriver, Guess, Race, RaceResult
from app.models.results import DriverPosition, Standings
from app.core.dependencies import get_db_session, oauth2_scheme
from app.core.config import settings

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload  # You can return the payload to use it in your route functions
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.get("/sessions", response_model=List[Race])
async def get_races(
    session: SessionDep,
    limit: Optional[int] = Query(
        None, description="Number of latest races to return, or all races if omitted"
    ),
    _=Depends(verify_token),
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
async def session_drivers(
    session_id: int,
    session: SessionDep,
    _=Depends(verify_token),
):
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
async def user_session_guess(
    guess: Guess,
    session: SessionDep,
    _=Depends(verify_token),
):
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
async def session_standing(
    session: SessionDep,
    session_key: int = Query(None, description="Session key of the requested results"),
    token_data: dict = Depends(verify_token),
):
    query_result = select(RaceResult).where(RaceResult.race_id == session_key)
    result = session.exec(query_result).first()
    print(result)
    query_drivers = []
    query_drivers.append(
        select(RaceDriver).where(
            and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == result.first_place_driver_number,
            )
        )
    )
    query_drivers.append(
        select(RaceDriver).where(
            and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == result.second_place_driver_number,
            )
        )
    )
    query_drivers.append(
        select(RaceDriver).where(
            and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == result.third_place_driver_number,
            )
        )
    )
    driver_numbers_in_top = []
    for pos, query in enumerate(query_drivers):
        driver_at_position = session.exec(query).first()
        print(driver_at_position)
        driver_numbers_in_top.append(
            DriverPosition(
                position=pos,
                driver_number=driver_at_position.driver_number,
                driver_name=driver_at_position.driver_name,
            )
        )

    return Standings(session_key=session_key, standings=driver_numbers_in_top)
