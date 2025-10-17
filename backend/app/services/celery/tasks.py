import logging
from datetime import datetime
from app.services.database.database_service import DatabaseService
from app.services.f1openapi.f1_api_service import F1API
from app.services.celery.celery_config import celery_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create service instances (these could be injected via DI container in the future)
f1_api = F1API()
db_service = DatabaseService(f1_api)

@celery_app.task
def update_database():
    """Runs periodic updates for missing sessions, drivers, and results."""
    logger.info("Starting database update task...")
    
    try:
        # Get current year dynamically
        current_year = str(datetime.now().year)
        
        # Sync data for current year
        result = db_service.sync_year_data(current_year)
        
        logger.info(f"Database update completed successfully: {result}")
        return {
            "status": "success",
            "year": current_year,
            "result": result.__dict__
        }
        
    except Exception as e:
        logger.error(f"Database update failed: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
        
@celery_app.task
def update_session_result():
    raise NotImplementedError("This task is not yet implemented.")