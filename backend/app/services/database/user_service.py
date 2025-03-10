from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session
from app.models.sql_models import User, Guess
from app.services.database.connector import MYSQLDB


class UserService:
    @staticmethod
    def add_user(session: Session, username: str, email: str):
        try:
            if UserService.get_user(session, username, email):
                print("User already added")
            else:
                new_user = User(username=username, email=email)
                session.add(new_user)
                session.commit()
                print(f"User {new_user} added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding user:", e)

    @staticmethod
    def get_user(session: Session, username: str, email: str):
        try:
            sql_filter = select(User).where(
                and_(User.email == email, User.username == username)
            )
            return session.exec(sql_filter).first()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")

    @staticmethod
    def add_guess(
        session: Session,
        guess: Guess,
    ):
        try:
            new_guess = Guess(
                user_id=guess.user_id,
                race_id=guess.race_id,
                position_1_driver_id=guess.position_1_driver_id,
                position_2_driver_id=guess.position_2_driver_id,
                position_3_driver_id=guess.position_3_driver_id,
            )
            session.add(new_guess)
            session.commit()
            print("Guess added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding guess:", e)
