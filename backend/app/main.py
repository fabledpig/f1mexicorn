from app.core.app_base import Application
from app.core.config import settings
from app.services.database_connector import get_database

app = Application(title=settings.app_name, version=settings.version)

app.add_event_handler("startup", get_database().connect)
app.add_event_handler("shutdown", get_database().close)
