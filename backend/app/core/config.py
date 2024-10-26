from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "F1 Mexicorn"
    version: str = "0.1.0"
    environment: str = "development"

    # dbg configuration later here

    # class Config:
    #     env_file = ".env"


settings = Settings()
