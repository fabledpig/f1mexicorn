from pydantic import BaseModel
from typing import List


class DriverPosition(BaseModel):
    position: int
    driver_number: int


class Standings(BaseModel):
    session_key: int
    standings: List[DriverPosition]
