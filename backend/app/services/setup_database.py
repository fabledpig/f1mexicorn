from app.services.database.database_service import DatabaseService
from app.services.f1openapi.f1_api_service import F1API
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    # Create service instances
    f1_api = F1API()
    db_service = DatabaseService(f1_api)
    
    try:
        # Sync data for 2025
        result = db_service.sync_year_data("2025")
        print(f"Sync completed: {result}")
        
    except Exception as e:
        print(f"Sync failed: {e}")
