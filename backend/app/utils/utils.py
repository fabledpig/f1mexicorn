import os
from dotenv import load_dotenv
from pathlib import Path


def load_env_variables():
    current_path = Path(__file__)
    secret_location = current_path.parent.parent.parent / ".env"
    load_dotenv(str(secret_location))


def get_google_auth_client_credentials():
    load_env_variables()
    # Access the API keys
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    return (client_id, client_secret)


def get_database_credentials():
    load_env_variables()
    return (os.getenv("MYSQL_USER"), os.getenv("MYSQL_PASSWORD"))
