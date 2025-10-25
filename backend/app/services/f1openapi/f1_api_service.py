# F1 OPEN API service

import requests
import time
import logging
from typing import Optional, Dict, List, Any

"""
Service class to interact with F1 open API
For now get the following info for basic functionality
- meetings
- drivers  
- sessions
"""

class F1API:
    """Service for interacting with the F1 Open API."""
    
    def __init__(self, base_url: str = "https://api.openf1.org/v1", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, retries: int = 3, backoff_factor: int = 2) -> Optional[List[Dict]]:
        """
        Make a GET request to the F1 API with retry logic.
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            retries: Number of retry attempts
            backoff_factor: Exponential backoff multiplier
            
        Returns:
            JSON response data or None if failed
        """
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                
                # Log error responses
                if response.status_code >= 400:
                    self.logger.error(f"API Error {response.status_code}: {response.text}")

                # Handle rate limiting (429 Too Many Requests)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    self.logger.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue  # Retry immediately after sleeping

                # Handle 5xx errors with retries
                if 500 <= response.status_code < 600:
                    if attempt < retries - 1:
                        wait_time = backoff_factor ** attempt
                        self.logger.warning(f"Server error {response.status_code}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        self.logger.error(f"Server error {response.status_code}. No more retries left.")
                        return None

                # Handle successful but empty responses
                if response.status_code == 200:
                    if not response.content.strip():  # Check if response is empty
                        self.logger.warning("API returned an empty response.")
                        return None
                    try:
                        return response.json()
                    except requests.exceptions.JSONDecodeError:
                        self.logger.warning("API returned invalid JSON.")
                        return None
                
                # Return response for other success cases
                return response.json()

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request failed: {e}")
                if attempt < retries - 1:
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)  # Exponential backoff before retry

        return None  # Return None if all retries fail

    def get_meetings(self, year: str) -> Optional[List[Dict]]:
        """Get all meetings in a given year."""
        params = {"year": year}
        return self._get("sessions", params)

    def get_sessions(self, year: str) -> Optional[List[Dict]]:
        """Get all sessions in a given year."""
        params = {"year": year}
        return self._get("sessions", params)

    def get_sessions_in_year(self, year: str) -> Optional[List[Dict]]:
        """Alias for get_sessions for backwards compatibility."""
        return self.get_sessions(year)

    def get_session_by_id(self, session_key: str) -> Optional[List[Dict]]:
        """Get session details by session key."""
        params = {"session_key": session_key}
        return self._get("sessions", params)

    def get_meeting_drivers(self, meeting_key: str) -> Optional[List[Dict]]:
        """Get drivers from a given meeting (weekend)."""
        params = {"meeting_key": meeting_key}
        return self._get("drivers", params)

    def get_session_drivers(self, session_key: str) -> Optional[List[Dict]]:
        """Get drivers for a given session (qualy, race, sprint)."""
        params = {"session_key": session_key}
        return self._get("drivers", params)

    def get_driver_at_position_in_session(self, session_key: str, position_number: int) -> Optional[Dict]:
        """
        Get driver at specific position in session.
        
        Args:
            session_key: Session identifier
            position_number: Position (1, 2, 3, etc.)
            
        Returns:
            Driver data for the final position or None
        """
        params = {
            "session_key": session_key,
            "position": position_number
        }
        
        # F1 open API returns the list of drivers associated with that
        # position throughout the race, so we only need the last element
        result = self._get("position", params)
        if not result:  # Prevents 'NoneType' errors
            self.logger.warning(f"No data for session {session_key}, position {position_number}")
            return None

        return result[-1] if result else None  # Return final position data