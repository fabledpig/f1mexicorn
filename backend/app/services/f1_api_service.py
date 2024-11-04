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

    def __init__(self, year=None, country=None):
        self._year = year

    @property
    def year(self):
        return self._year

    @year.setter
    def country(self, value):
        self._year = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    def _get(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        return response.json()

    def get_meetings(self):
        params = {}
        if self._year:
            params["year"] = self._year

        return self._get("meetings", params)

    def get_drivers(self, meeting_key):
        params = {}
        params["meeting_key"] = meeting_key
        return self._get("drivers", params)

    # only get
    def get_sessions(self):
        params = {}
        if self._year:
            params["year"] = self._year
        return self._get("sessions", params)
