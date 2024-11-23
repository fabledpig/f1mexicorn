# F1 OPEN API tempering

import requests
import time

"""
Utility class to interact with F1 open API
For now get the following info for basic functionality
- meetings
- drives
- sessions
"""


class F1API:
    BASE_URL = "https://api.openf1.org/v1"

    @staticmethod
    def _get(endpoint, params=None):
        url = f"{F1API.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        # Check if rate limit was exceeded (HTTP status code 429)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
            time.sleep(retry_after)
            return F1API._get(endpoint, params)

        return response.json()

    # Get all meetings in a given year
    @staticmethod
    def get_meetings(year):
        params = {}
        params["year"] = year
        return F1API._get("sessions", params)

    # Get all sessions in a given year
    @staticmethod
    def get_sessions(year):
        params = {}
        params["year"] = year
        return F1API._get("sessions", params)

    @staticmethod
    def get_session_by_id(session_key):
        params = {}
        params["session_key"] = session_key
        return F1API._get("sessions", params)

    # Get drivers from a given meeting (weekend)
    @staticmethod
    def get_meeting_drivers(meeting_key):
        params = {}
        params["meeting_key"] = meeting_key
        return F1API._get("drivers", params)

    # Get drivers for a given session (qualy, race, sprint)
    @staticmethod
    def get_session_drivers(session_key):
        params = {}
        params["session_key"] = session_key
        return F1API._get("drivers", params)

    @staticmethod
    def get_driver_at_position_in_session(session_key, position_number):
        params = {}
        params["session_key"] = session_key
        params["position"] = position_number
        # unfortunately F1 open api return the list of drivers associated with that
        # position throuhgout the race, so we only need the last elemen
        return F1API._get("position", params)[:1][0]
