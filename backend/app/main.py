from app.core.app_base import Application
from app.core.config import settings

app = Application(title=settings.app_name, version=settings.version)

# Optional: add event handlers or middlewares
app.add_middlewares()
app.add_event_handlers()
