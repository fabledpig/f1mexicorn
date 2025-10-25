from sqlmodel import Column, Integer, String, SQLModel, Field, Relationship, ForeignKey
from typing import Optional, List


class User(SQLModel, table=True):
    username: str = Field(max_length=50)
    email: str = Field(max_length=100, unique=True, primary_key=True)
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
    team: str = Field(max_length=50, nullable=True)

    race: "Race" = Relationship(back_populates="race_drivers")


class Guess(SQLModel, table=True):
    guess_id: Optional[int] = Field(default=None, primary_key=True)
    user_email: str = Field(
        max_length=100,
        sa_column=Column(String(100), ForeignKey("user.email", ondelete="CASCADE"), nullable=False)
    )
    race_id: int = Field(
        sa_column=Column(Integer, ForeignKey("race.race_id", ondelete="CASCADE"))
    )
    position_1_driver_id: int = Field(sa_column = Column(Integer, ForeignKey("racedriver.race_driver_id", ondelete="CASCADE")))
    position_2_driver_id: int = Field(sa_column = Column(Integer, ForeignKey("racedriver.race_driver_id", ondelete="CASCADE")))
    position_3_driver_id: int = Field(sa_column = Column(Integer, ForeignKey("racedriver.race_driver_id", ondelete="CASCADE")))

    user: User = Relationship(back_populates="guesses")
    race: Race = Relationship(back_populates="guesses")


class RaceResult(SQLModel, table=True):
    race_result_id: Optional[int] = Field(default=None, primary_key=True)
    race_id: int = Field(
        sa_column=Column(
            Integer, ForeignKey("race.race_id", ondelete="CASCADE"),
        )
    )
    position_1_driver_id: int
    position_2_driver_id: int
    position_3_driver_id: int

    race: "Race" = Relationship(back_populates="race_result")
