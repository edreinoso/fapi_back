from core.ports import UEFAPlayerStatsRepository
from core.measurement_service import MeasurementService

class UEFAService:
    def __init__(self, uefa_repository: UEFAPlayerStatsRepository, measurement_repository: MeasurementService): 
        self.uefa_repository = uefa_repository
        self.measurement_repository = measurement_repository

    def get_all_player_matches_stats_from_uefa(self) -> list:
        pass

    def get_all_player_stats_from_uefa(self) -> list:
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