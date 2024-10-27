import os
from dotenv import load_dotenv
from pathlib import Path

CURENT_PATH = Path(__file__)


def get_google_auth_client_credentials():
    secret_location = CURENT_PATH.parent.parent.parent / ".env"
    load_dotenv(str(secret_location))

    # Access the API keys
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    return (client_id, client_secret)
