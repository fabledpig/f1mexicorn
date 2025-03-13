
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from app.models.sql_models import RaceDriver


class RaceDriverService:
    """
    Queries associated with any type of F1 Session Drivers
    """

    @staticmethod
    def get_all_session_drivers(session: Session):
        try:
            query = select(RaceDriver)
            all_session_drivers = session.exec(query).all()
            return all_session_drivers
        except SQLAlchemyError as e:
            session.rollback()
            print("Error fetchin all drivers:", e)    
        
    @staticmethod
    def add_session_driver(
        session: Session, session_key, driver_name, driver_number, nationality, team
    ):
        try:
            query = and_(
                RaceDriver.race_id == session_key,
                RaceDriver.driver_number == driver_number,
            )

            existing_driver = session.exec(select(RaceDriver).where(query)).first()
            if existing_driver:
                print("Driver already added")
                return
            new_driver = RaceDriver(
                race_id=session_key,
                driver_name=driver_name,
                driver_number=driver_number,
                nationality=nationality,
                team=team,
            )
            session.add(new_driver)
            session.commit()
            print("Driver added successfully")
        except SQLAlchemyError as e:
            session.rollback()
            print("Error adding driver:", e)

    @staticmethod
    def get_session_drivers(session: Session, session_id: int):
        try:
            sql_filter = select(RaceDriver).where(RaceDriver.race_id == session_id)
            return session.exec(sql_filter).all()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"An error occurred: {e}")
