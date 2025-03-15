# adapters/api_adapter.py
import http.client
import json

class UEFAPlayerStatsRepository:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def get_all_player_stats(self) -> dict:
        conn = http.client.HTTPSConnection("gaming.uefa.com")
        conn.request("GET", self.endpoint_url)
        res = conn.getresponse()
        data = res.read()
        players_data = json.loads(data.decode("utf-8"))
        print(type(players_data['data']['value']['playerList']))
        return players_data['data']['value']['playerList']
    
    # Players that are still participating in the tournament
    def get_current_player_stats():
        pass