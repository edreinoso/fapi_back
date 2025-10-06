"""
UEFA API Client for fetching Champions League data
"""
import http.client
import json
import logging
import time
from typing import Dict, Any, Optional


class UEFAApiClient:
    """Client for communicating with UEFA's fantasy football API"""
    
    BASE_HOST = "gaming.uefa.com"
    FIXTURES_ENDPOINT = "/en/uclfantasy/services/feeds/fixtures/fixtures_80_en.json"
    PLAYERS_ENDPOINT = "/en/uclfantasy/services/feeds/players/players_80_en_2.json"
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def _make_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to UEFA API
        
        Args:
            endpoint: API endpoint to call
            
        Returns:
            Parsed JSON response or None if failed
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Making request to {self.BASE_HOST}{endpoint}")
            
            conn = http.client.HTTPSConnection(self.BASE_HOST)
            conn.request("GET", endpoint)
            
            response = conn.getresponse()
            
            if response.status != 200:
                self.logger.error(f"HTTP {response.status}: {response.reason}")
                return None
            
            data = response.read()
            parsed_data = json.loads(data.decode("utf-8"))
            
            end_time = time.time()
            self.logger.info(f"Request completed in {end_time - start_time:.2f} seconds")
            
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error making request to {endpoint}: {str(e)}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
    
    def fetch_fixtures_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch fixtures data from UEFA API
        
        Returns:
            Raw fixtures data from API
        """
        self.logger.info("Fetching UEFA fixtures data")
        return self._make_request(self.FIXTURES_ENDPOINT)
    
    def fetch_players_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch players data from UEFA API
        
        Returns:
            Raw players data from API
        """
        self.logger.info("Fetching UEFA players data")
        return self._make_request(self.PLAYERS_ENDPOINT)