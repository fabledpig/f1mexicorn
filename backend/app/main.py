from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.app_base import Application
from app.core.config import settings
from app.services.database.connector import get_db_manager
from app.core.container import get_container
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application startup and shutdown.
    """
    # Startup
    logger.info("Starting up F1 application...")
    
    # Initialize the service container
    container = get_container()
    container.initialize()
    
    logger.info("F1 application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down F1 application...")
    
    # Close database connections
    get_db_manager().close()
    
    # Reset container if needed
    if hasattr(app.state, 'container'):
        app.state.container.reset()
    
    logger.info("F1 application shutdown complete")


app = Application(title=settings.app_name, version=settings.version, lifespan=lifespan)
