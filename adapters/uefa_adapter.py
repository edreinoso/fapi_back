# adapters/api_adapter.py
import http.client
import json

class UEFAPlayerStatsRepository:
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def get_all_player_stats(self) -> list:
        conn = http.client.HTTPSConnection("gaming.uefa.com")
        conn.request("GET", self.endpoint_url)
        res = conn.getresponse()
        data = res.read()
        players_data = json.loads(data.decode("utf-8"))
        return players_data['data']['value']['playerList']
    
    def get_all_matches_per_player_stats(self, player_id: str) -> tuple[list, list]:
        conn = http.client.HTTPSConnection("gaming.uefa.com")
        conn.request("GET", f"/en/uclfantasy/services/feeds/popupstats/popupstats_70_{player_id}.json")
        res = conn.getresponse()
        data = res.read()
        players_data = json.loads(data.decode("utf-8"))
        fixtures = players_data['data']['value']['fixtures']
        stats = players_data['data']['value']['stats']
        points = players_data['data']['value']['points']
        return fixtures, stats, points
    
    # Players that are still participating in the tournament
    def get_current_player_stats():
        pass