**Setup and run the f1 mexicorn backend application**
- pip install -r requirements.txt
- Go into /backend folder and `uvicorn app.main:app --reload`

celery -A app.services.celery.celery_config.celery_app worker --loglevel=info
celery -A app.services.celery.celery_config.celery_app beat --loglevel=info