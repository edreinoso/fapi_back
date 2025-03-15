# core/player_service.py
from core.ports import DDBPlayerStatsRepository
from core.ports import UEFAPlayerStatsRepository
from datetime import datetime, timezone


class PlayerService:
    def __init__(self, stats_repository: DDBPlayerStatsRepository, uefa_repository: UEFAPlayerStatsRepository):
        self.stats_repository = stats_repository
        self.uefa_repository = uefa_repository
        self.skill_map = {
            1: "goal keepers",
            2: "defenders",
            3: "midfielders",
            4: "attackers"
        }

    def put_player_total_score(self, player_name: str, player_id: str, player_goals: str, player_assists: str, team: str, position: str) -> str:
        # update players in fapi ddb
        self.stats_repository.put_player_total_score(player_name, player_id, player_goals, player_assists, team, position)
        
        return "hello world"
    
    def get_all_player_stats_from_uefa(self) -> dict:
        # retrieve players from uefa
        list_of_players = []
        players_data = self.uefa_repository.get_all_player_stats()

        for player in players_data:
            # Transform the skill number to its description
            skill_description = self.skill_map.get(player.get('skill', 0), 'unknown')

            list_of_players.append({
                'id': player.get('id', ''),
                'name': player.get('pDName', '').lower(),
                'goals': player.get('gS', ''),
                'assist': player.get('assist', ''),
                'team': player.get('tName', ''),
                'position': skill_description
            })

        return list_of_players

    def get_player_stats_from_ddb(self, player_name: str, attributes: str) -> dict:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
        stats = self.stats_repository.get_player_stats(player_name, today, attributes)
        if not stats:
            return {"error": "Player not found"}

        return stats