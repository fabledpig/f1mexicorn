from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    # from Google SSO data
    return [
        {"user_id": 1, "name": "Alice"},
    ]


@router.post("/users/", tags=["users"])
async def create_user(name: str):
    return {"user_id": 3, "name": name}
