from celery import Celery

# Configure Celery with Redis as the broker (update with your Redis URL)
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  
    backend="redis://localhost:6379/0"
)

celery_app.conf.timezone = "UTC"

# Auto-discover tasks in 'app.services.celery'
celery_app.autodiscover_tasks(["app.services.celery"])

# Celery Beat (for periodic tasks)
celery_app.conf.beat_schedule = {
    "update_database_hourly": {
        "task": "app.services.celery.tasks.update_database",
        "schedule": 3600.0,
    },
}
