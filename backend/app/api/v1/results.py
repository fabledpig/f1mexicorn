from fastapi import Depends, APIRouter
from typing import List
from typing_extensions import Annotated
from sqlmodel import Session
from app.models.sql_models import User

from app.core.dependencies import get_db_session

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]


@router.get("/winners", response_model=List[User])
async def get_winners(session: SessionDep):
    pass
