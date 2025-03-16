# core/player_service.py
import time
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

    def recreate_ddb_table(self) -> str:
        self.stats_repository.delete_table()
        self.stats_repository.describe_table()
        self.stats_repository.create_table()
        return "Table has been recreated"
        
    def update_ddb_table_with_latest_player_data(self) -> str:
        
        # delete ddb table
        self.recreate_ddb_table()
        
        # get all players from uefa
        list_of_players = self.get_all_player_stats_from_uefa()

        # update players in fapi ddb
        for player in list_of_players:
            self.stats_repository.put_player_total_scores_ap2(player['name'], player['id'], player['goals'], player['assist'], player['team'], player['position'])

        return "All players with access pattern two have been updated"

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