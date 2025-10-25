from datetime import datetime, timezone
import logging
import dateutil
from sqlmodel import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
import sqlmodel
from app.models.sql_models import (
    User,
    Guess,
    RaceDriver,
    Race
)


class UserService:
    """Service for managing user operations."""
    
    def add_user(self, session: Session, username: str, email: str):
        try:
            if self.get_user(session, email):
                print("User already added")
            else:
                new_user = User(username=username, email=email)
                session.add(new_user)
                session.commit()
                print(f"User {new_user} added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding user:", e)

    def get_user(self, session: Session, email: str):
        try:
            sql_filter = select(User).where(
                and_(User.email == email)
            )
            return session.exec(sql_filter).first()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")


    def get_guess(
        self,
        session: Session,
        user_email: str
    ) -> Guess:
        try:
            sql_filter = select(Guess).where(Guess.user_email == user_email)
            return session.exec(sql_filter).first()  # Unpack the tuple
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def add_guess(
        self,
        session: Session,
        guess: Guess,
    ):
        # Validate guess drivers
        sql_filter_1 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_1_driver_id
        ))
        sql_filter_2 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_2_driver_id
        ))
        sql_filter_3 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_3_driver_id
        ))
        
        if not (session.exec(sql_filter_1).first() and  session.exec(sql_filter_2).first() and  session.exec(sql_filter_3).first()):
            raise Exception("Invalid guess, race and drivers don't match")
            
        # Validate guess time
        sql_filter_race = sqlmodel.select(Race).where(Race.race_id == guess.race_id)
        race = session.exec(sql_filter_race).first()
    
        if race is None:
            raise Exception("Invalid guess, race does not exist")
        elif dateutil.parser.isoparse(race.race_date) <= datetime.now(timezone.utc):
            raise Exception("Invalid guess, race already STARTED or FINISHED")
        
        # Validate user has no guess yet for this event
        existing_guess = self.get_guess(session, guess.user_email)
        if self.get_guess(session, guess.user_email) is not None:
            # Modify the current guess
            existing_guess.position_1_driver_id = guess.position_1_driver_id
            existing_guess.position_2_driver_id = guess.position_2_driver_id
            existing_guess.position_3_driver_id = guess.position_3_driver_id
            try:
                session.commit()
                session.refresh(existing_guess)
            except SQLAlchemyError as e:
                session.rollback()
                logging.error(f"Error updating guess: {e}")
                raise
            logging.info(f"Guess updated successfully for user: {guess.user_email}")
        else:
        
            new_guess = Guess(
                user_email=guess.user_email,
                race_id=guess.race_id,
                position_1_driver_id=guess.position_1_driver_id,
                position_2_driver_id=guess.position_2_driver_id,
                position_3_driver_id=guess.position_3_driver_id,
            )
            session.add(new_guess)
            session.commit()
            logging.info(f"Guess added successfully with guess_id: {new_guess.guess_id}")