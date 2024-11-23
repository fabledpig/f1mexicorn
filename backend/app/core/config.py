from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "F1 Mexicorn"
    version: str = "0.1.0"
    environment: str = "development"

    client_id: str
    client_secret: str
    mysql_user: str
    mysql_password: str
    host_name: str
    database_name: str
    celery_broker_url: str
    celery_result_backend: str
    secret_key: str
    discord_hook: str

    class Config:
        # Need to be at the working directory from where the fastapi application is started
        env_file = ".env"


settings = Settings()
