from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from app.models.sql_models import RaceDriver, User, Guess


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

    def add_guess(
        self,
        session: Session,
        guess: Guess,
    ):
        # Check whether the guess is correct:
        sql_filter_1 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_1_driver_id
        ))
        sql_filter_2 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_2_driver_id
        ))
        sql_filter_3 = select(RaceDriver).where(and_(
            RaceDriver.race_id == guess.race_id, RaceDriver.driver_number == guess.position_3_driver_id
        ))
        
        if session.exec(sql_filter_1).first() and  session.exec(sql_filter_2).first() and  session.exec(sql_filter_3).first():
            new_guess = Guess(
                user_email=guess.user_email,
                race_id=guess.race_id,
                position_1_driver_id=guess.position_1_driver_id,
                position_2_driver_id=guess.position_2_driver_id,
                position_3_driver_id=guess.position_3_driver_id,
            )
            session.add(new_guess)
            session.commit()
            print(f"Guess added successfully with guess_id: {new_guess.guess_id}")
        else:
            raise Exception("Invalid guess, race and drivers don't match")