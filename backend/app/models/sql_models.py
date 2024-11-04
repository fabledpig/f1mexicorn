from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    email: str = Field(max_length=100, unique=True)


class Driver(SQLModel, table=True):
    driver_id: Optional[int] = Field(default=None, primary_key=True)
    driver_name: str = Field(max_length=100)
    nationality: Optional[str] = Field(max_length=50)
    team: Optional[str] = Field(max_length=50)


class Race(SQLModel, table=True):
    race_id: Optional[int] = Field(default=None, primary_key=True)
    race_name: str = Field(max_length=100)
    race_type: str = Field(max_length=100)
    race_date: str


class RaceResult(SQLModel, table=True):
    result_id: Optional[int] = Field(default=None, primary_key=True)
    race_id: int = Field(foreign_key="race.race_id")
    driver_id: int = Field(foreign_key="driver.driver_id")
    position: int


class Guess(SQLModel, table=True):
    guess_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    race_id: int = Field(foreign_key="race.race_id")
    position_1_driver_id: int = Field(foreign_key="driver.driver_id")
    position_2_driver_id: int = Field(foreign_key="driver.driver_id")
    position_3_driver_id: int = Field(foreign_key="driver.driver_id")


class RaceDriver(SQLModel, table=True):
    race_driver_id: Optional[int] = Field(default=None, primary_key=True)
    race_id: int = Field(foreign_key="race.race_id")
    driver_id: int = Field(foreign_key="driver.driver_id")
