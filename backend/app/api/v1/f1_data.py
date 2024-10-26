from fastapi import APIRouter

router = APIRouter()


@router.get("/f1", tags=["f1"])
async def read_items():
    pass
