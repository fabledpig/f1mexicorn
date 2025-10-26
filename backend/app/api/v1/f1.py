import logging
from typing import List, Optional
from sqlmodel import Session
from typing_extensions import Annotated

from fastapi import Depends, Path, Query, APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy.exc import SQLAlchemyError

from app.models.sql_models import RaceDriver, Race, Guess
from app.models.pydantic_models import Standings
from app.core.dependencies import (
    get_db_session, 
    verify_token,
    get_race_service,
    get_user_service,
    get_race_driver_service,
    get_race_result_service,
    event_queue
)
from app.services.database.race_service import RaceService
from app.services.database.user_service import UserService
from app.services.database.race_driver_service import RaceDriverService
from app.services.database.race_result_service import RaceResultService

router = APIRouter()

# Type aliases for dependency injection
SessionDep = Annotated[Session, Depends(get_db_session)]
RaceServiceDep = Annotated[RaceService, Depends(get_race_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
RaceDriverServiceDep = Annotated[RaceDriverService, Depends(get_race_driver_service)]
RaceResultServiceDep = Annotated[RaceResultService, Depends(get_race_result_service)]


@router.get("/sessions", response_model=List[Race])
async def get_races(
    session: SessionDep,
    race_service: RaceServiceDep,
    limit: int = Query(
        0, description="Number of latest races to return, or all races if omitted"
    ),
    _=Depends(verify_token),
):
    try:
        races = race_service.get_races(session, limit)

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
async def get_session_drivers(
    session_id: int,
    session: SessionDep,
    race_driver_service: RaceDriverServiceDep,
    _=Depends(verify_token),
):
    try:
        session_drivers = race_driver_service.get_session_drivers(session, session_id)
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

@router.get("/guess/{event_id}", response_model=Optional[Guess])
async def get_user_guess(
    session: SessionDep,
    user_service: UserServiceDep,
    verify_token: str = Depends(verify_token),
    event_id: int = Path(..., description="Session ID for which to get the user's guess"),
):
    try:
        user_email = verify_token.get("email")
        user_guess = user_service.get_guess(session, user_email, event_id)
        print(user_guess)
        return user_guess
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
async def post_user_guess(
    guess: Guess,
    session: SessionDep,
    user_service: UserServiceDep,
    _: str = Depends(verify_token),
):
    try:
        user_service.add_guess(session, guess)
        return guess

    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )

    except Exception as e:
        logging.error(f"Error occurred while adding guess: {repr(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {repr(e)}",
        )


# TODO how to do this, always fetch from F1 openapi,
# or cache some and only request at regular intervals, probably need to use redis here
@router.get("/session_standing", response_model=Standings)
async def get_session_standing(
    session: SessionDep,
    race_result_service: RaceResultServiceDep,
    session_key: int = Query(None, description="Session key of the requested results"),
    _=Depends(verify_token),
):
    try:
        driver_numbers_in_top = race_result_service.get_race_standing(session, session_key)

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
    
    logging.info(f"Retrieved standings for session {session_key}: {driver_numbers_in_top}")
    return Standings(session_key=session_key, standings=driver_numbers_in_top)


async def event_stream(request: Request):
    while True:
        data = await event_queue.get()
        logging.info(f'ARRIVED DATA: {data}')
        yield f"data: {data}\n\n"

# Experimental sse endpoint
@router.get("/session_standing_sse" )
async def get_session_standing_sse(request: Request):
    return StreamingResponse(event_stream(request), media_type="text/event-stream")