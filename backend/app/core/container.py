"""
Dependency injection container for the F1 application.
Provides centralized service creation and dependency management.
"""

from typing import Dict, Any
from functools import lru_cache
import logging

from app.services.f1openapi.f1_api_service import F1API
from app.services.database.database_service import DatabaseService
from app.services.database.race_service import RaceService
from app.services.database.race_driver_service import RaceDriverService
from app.services.database.race_result_service import RaceResultService
from app.services.database.user_service import UserService

logger = logging.getLogger(__name__)

class ServiceContainer:
    """Container for managing application services and their dependencies."""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize all services with their dependencies."""
        if self._initialized:
            return
            
        logger.info("Initializing service container...")
        
        # Initialize core services
        self._services['f1_api'] = F1API()
        self._services['database_service'] = DatabaseService(self._services['f1_api'])
        self._services['race_service'] = RaceService()
        self._services['race_driver_service'] = RaceDriverService()
        self._services['race_result_service'] = RaceResultService()
        self._services['user_service'] = UserService()
        
        self._initialized = True
        logger.info("Service container initialized successfully")
    
    def get_f1_api(self) -> F1API:
        """Get F1 API service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['f1_api']
    
    def get_database_service(self) -> DatabaseService:
        """Get database synchronization service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['database_service']
    
    def get_race_service(self) -> RaceService:
        """Get race service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['race_service']
    
    def get_race_driver_service(self) -> RaceDriverService:
        """Get race driver service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['race_driver_service']
    
    def get_race_result_service(self) -> RaceResultService:
        """Get race result service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['race_result_service']
    
    def get_user_service(self) -> UserService:
        """Get user service instance."""
        if not self._initialized:
            self.initialize()
        return self._services['user_service']

    def reset(self) -> None:
        """Reset the container (mainly for testing)."""
        self._services.clear()
        self._initialized = False


# Global container instance
@lru_cache(maxsize=1)
def get_container() -> ServiceContainer:
    """Get the global service container instance."""
    return ServiceContainer()


# FastAPI dependency functions
def get_f1_api() -> F1API:
    """FastAPI dependency for F1 API service."""
    return get_container().get_f1_api()


def get_database_service() -> DatabaseService:
    """FastAPI dependency for database service."""
    return get_container().get_database_service()


def get_race_service() -> RaceService:
    """FastAPI dependency for race service."""
    return get_container().get_race_service()


def get_race_driver_service() -> RaceDriverService:
    """FastAPI dependency for race driver service."""
    return get_container().get_race_driver_service()


def get_race_result_service() -> RaceResultService:
    """FastAPI dependency for race result service."""
    return get_container().get_race_result_service()


def get_user_service() -> UserService:
    """FastAPI dependency for user service."""
    return get_container().get_user_service()