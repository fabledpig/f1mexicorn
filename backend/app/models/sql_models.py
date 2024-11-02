from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Initialize the base class for declarative tables
Base = declarative_base()


# Users Table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    guesses = relationship("Guess", back_populates="user", cascade="all, delete")


# Drivers Table
class Driver(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    driver_name = Column(String(100), nullable=False)
    nationality = Column(String(50))
    team = Column(String(50))

    race_results = relationship(
        "RaceResult", back_populates="driver", cascade="all, delete"
    )
    guesses_position_1 = relationship(
        "Guess", foreign_keys="Guess.position_1_driver_id"
    )
    guesses_position_2 = relationship(
        "Guess", foreign_keys="Guess.position_2_driver_id"
    )
    guesses_position_3 = relationship(
        "Guess", foreign_keys="Guess.position_3_driver_id"
    )


# Races Table
class Race(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True, autoincrement=True)
    race_name = Column(String(100), nullable=False)
    race_type = Column(String(100), nullable=False)
    race_date = Column(Date, nullable=False)

    race_results = relationship(
        "RaceResult", back_populates="race", cascade="all, delete"
    )
    guesses = relationship("Guess", back_populates="race", cascade="all, delete")
    race_drivers = relationship(
        "RaceDriver", back_populates="race", cascade="all, delete"
    )


# Race Results Table
class RaceResult(Base):
    __tablename__ = "race_results"

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id", ondelete="CASCADE"))
    position = Column(Integer, nullable=False)

    race = relationship("Race", back_populates="race_results")
    driver = relationship("Driver", back_populates="race_results")


# Guesses Table
class Guess(Base):
    __tablename__ = "guesses"

    guess_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))
    position_1_driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    position_2_driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    position_3_driver_id = Column(Integer, ForeignKey("drivers.driver_id"))

    user = relationship("User", back_populates="guesses")
    race = relationship("Race", back_populates="guesses")
    driver1 = relationship("Driver", foreign_keys=[position_1_driver_id])
    driver2 = relationship("Driver", foreign_keys=[position_2_driver_id])
    driver3 = relationship("Driver", foreign_keys=[position_3_driver_id])


# Race Drivers Table
class RaceDriver(Base):
    __tablename__ = "race_drivers"

    race_driver_id = Column(Integer, primary_key=True, autoincrement=True)
    race_id = Column(Integer, ForeignKey("races.race_id", ondelete="CASCADE"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id", ondelete="CASCADE"))

    race = relationship("Race", back_populates="race_drivers")
    driver = relationship("Driver")
