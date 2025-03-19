from core.ports import UEFAPlayerStatsRepository
from core.measurement_service import MeasurementService

class UEFAService:
    def __init__(self, uefa_repository: UEFAPlayerStatsRepository, measurement_repository: MeasurementService): 
        self.uefa_repository = uefa_repository
        self.measurement_repository = measurement_repository

    def get_all_player_matches_stats_from_uefa(self) -> list:
        list_of_players_matches = []
        players_data = self.get_all_player_stats_from_uefa()

        for player in players_data:
            fixtures, stats = self.uefa_repository.get_all_matches_per_player_stats(player['id'])
            
            for matches in range(0, len(fixtures)):
                match_id = fixtures[matches]['mId']
                goals_scored = stats[matches]['gS']
                assists = stats[matches]['gA']
                match_date = fixtures[matches]['dateTime']
                
                list_of_players_matches.append({
                    'player_name': player['name'],
                    'match_id': match_id,
                    'goals': goals_scored,
                    'assists': assists,
                    'date_time': match_date
                })


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