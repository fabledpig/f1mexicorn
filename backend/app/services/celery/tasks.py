import logging
from app.core.dependencies import get_db_session  # Function to get a database session
from app.services.database.database_service import DatabaseService
from app.services.celery.celery_config import celery_app
from app.services.database.connector import MYSQLDB

logging.basicConfig(level=logging.INFO)

mysqldb = MYSQLDB()
    

@celery_app.task
def update_database():
    """Runs periodic updates for missing sessions, drivers, and results."""
    logging.info("Updating database with missing sessions, drivers, and results...")
    DatabaseService.add_missing_sessions_in_year(mysqldb.get_session(), "2024")  # Update year dynamically if needed
    DatabaseService.add_missing_session_drivers(mysqldb.get_session())
    DatabaseService.add_missing_session_results(mysqldb.get_session())
    logging.info("Database update completed.")