from celery import Celery

# Configure Celery with Redis as the broker (update with your Redis URL)
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    # Windows-specific settings
    worker_pool='solo',  # Use solo pool on Windows
    task_always_eager=False,
    task_eager_propagates=True,
)
# Auto-discover tasks in 'app.services.celery'
celery_app.autodiscover_tasks(["app.services.celery"])

# Celery Beat (for periodic tasks)
celery_app.conf.beat_schedule = {
    "update_database": {
        "task": "app.services.celery.tasks.update_database",
        "schedule": 600.0,
    },
    "update_session_result": {
        "task": "app.services.celery.tasks.update_session_result",
        "schedule": 30.0,
    },
}
