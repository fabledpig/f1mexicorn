from fastapi import APIRouter

router = APIRouter()


@router.get("/f1", tags=["f1"])
async def sessions():
    pass


@router.get("/f1", tags=["f1"])
async def latest_session():
    pass


@router.get("/f1", tags=["f1"])
async def all_drivers():
    pass


@router.post("/f1", tags=["f1"])
async def session_drivers():
    pass


@router.post("/f1", tags=["f1"])
async def user_session_guess():
    pass
