from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import User, Guess
from app.services.database.connector import MYSQLDB


class UserService:
    @staticmethod
    def add_user(db: MYSQLDB, username, email):
        with db.get_session() as session:
            try:
                new_user = User(username=username, email=email)
                session.add(new_user)
                session.commit()
                print("User added successfully")
            except SQLAlchemyError as e:
                session.rollback()
                print("Error adding user:", e)

    @staticmethod
    def add_guess(
        db: MYSQLDB,
        guess: Guess,
    ):
        with db.get_session() as session:
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
