# adapters/api_adapter.py
import requests

class APIPlayerStatsRepository:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_player_stats(self, player_id: str) -> dict:
        response = requests.get(f"{self.base_url}/players/{player_id}/stats")
        return response.json() if response.status_code == 200 else {}