# F1 OPEN API tempering

import requests

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

    # Get drivers from a given meeting (weekend)
    @staticmethod
    def get_meeting_drivers(meeting_key):
        params = {}
        params["meeting_key"] = meeting_key
        return F1API._get("drivers", params)

    # Get rivers for a given session (qualy, race, sprint)
    @staticmethod
    def get_session_drivers(session_key):
        params = {}
        params["session_key"] = session_key
        return F1API._get("drivers", params)
