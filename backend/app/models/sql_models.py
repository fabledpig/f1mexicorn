from sqlmodel import Column, Integer, SQLModel, Field, Relationship, ForeignKey
from typing import Optional, List


class User(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    email: str = Field(max_length=100, unique=True)

    guesses: List["Guess"] = Relationship(back_populates="user", cascade_delete=True)


class Race(SQLModel, table=True):
    race_id: Optional[int] = Field(default=None, primary_key=True)
    race_name: str = Field(max_length=100)
    race_type: str = Field(max_length=100)
    race_date: str

    race_drivers: List["RaceDriver"] = Relationship(
        back_populates="race", cascade_delete=True
    )
    guesses: List["Guess"] = Relationship(back_populates="race", cascade_delete=True)
    race_result: List["RaceResult"] = Relationship(
        back_populates="race", cascade_delete=True
    )


class RaceDriver(SQLModel, table=True):
    race_driver_id: Optional[int] = Field(default=None, primary_key=True)
    race_id: int = Field(
        sa_column=Column(Integer, ForeignKey("race.race_id", ondelete="CASCADE"))
    )
    driver_number: int
    driver_name: str = Field(max_length=100)
    nationality: str = Field(max_length=50, nullable=True)
    team: str = Field(max_length=50, nullable=True)

    race: "Race" = Relationship(back_populates="race_drivers")


class Guess(SQLModel, table=True):
    guess_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    race_id: int = Field(foreign_key="race.race_id")
    position_1_driver_id: int = Field(foreign_key="racedriver.race_driver_id")
    position_2_driver_id: int = Field(foreign_key="racedriver.race_driver_id")
    position_3_driver_id: int = Field(foreign_key="racedriver.race_driver_id")

    user: User = Relationship(back_populates="guesses")
    race: Race = Relationship(back_populates="guesses")


class RaceResult(SQLModel, table=True):
    race_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("race.race_id", ondelete="CASCADE"), primary_key=True
        )
    )
    first_place_driver_number: int
    second_place_driver_number: int
    third_place_driver_number: int

    race: "Race" = Relationship(back_populates="race_result")
