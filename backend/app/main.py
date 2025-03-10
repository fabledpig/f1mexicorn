from app.core.app_base import Application
from app.core.config import settings
from app.services.database.connector import MYSQLDB

app = Application(title=settings.app_name, version=settings.version)

db_manager = MYSQLDB()


@app.on_event("startup")
def on_startup():
    app.state.db = db_manager


@app.on_event("shutdown")
def on_shutdown():
    app.state.db.close()
