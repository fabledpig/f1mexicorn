from fastapi import Depends, APIRouter, HTTPException, Query, status
from typing import Optional
from typing_extensions import Annotated
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import Guess
from app.services.database.race_result_service import RaceResultService

from app.core.dependencies import get_db_session, verify_token

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/winners", response_model=Optional[Guess])
async def get_winners(
    session: SessionDep,
    session_key: int = Query(None, description="Session key of the requested results"),
    _=Depends(verify_token),
):
    try:
        winning_guess = RaceResultService.get_winning_guess(session, session_key)
        return winning_guess
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error occurred: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An unexpected error occurred: {str(e)}",
        )
    
