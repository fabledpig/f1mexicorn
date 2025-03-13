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
    def _get(endpoint, params=None, retries=3, backoff_factor=2):
        url = f"{F1API.BASE_URL}/{endpoint}"
        
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=30)
                
                # Log error responses
                if response.status_code >= 400:
                    print(f"Error {response.status_code}: {response.text}")

                # Handle rate limiting (429 Too Many Requests)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue  # Retry immediately after sleeping

                # Handle 5xx errors with retries
                if 500 <= response.status_code < 600:
                    if attempt < retries - 1:
                        wait_time = backoff_factor ** attempt
                        print(f"Server error {response.status_code}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"Server error {response.status_code}. No more retries left.")
                        return None

                # Handle successful but empty responses
                if response.status_code == 200:
                    if not response.content.strip():  # Check if response is empty
                        print("Warning: API returned an empty response.")
                        return None
                    try:
                        return response.json()
                    except requests.exceptions.JSONDecodeError:
                        print("Warning: API returned invalid JSON.")
                        return None
                
                # Return response for other success cases
                return response.json()

            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
                time.sleep(backoff_factor ** attempt)  # Exponential backoff before retry

        return None  # Return None if all retries fail

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
        result = F1API._get("position", params)
        if not result:  # Prevents 'NoneType' errors
            print(f"No data for session {session_key}, position {position_number}")
            return None

        return result[:1][0] if result else None  # Ensures result is not None