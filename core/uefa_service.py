import time
from core.ports import UEFAPlayerStatsRepository
from core.measurement_service import MeasurementService

class UEFAService:
    def __init__(self, uefa_repository: UEFAPlayerStatsRepository, measurement_repository: MeasurementService): 
        self.uefa_repository = uefa_repository
        self.measurement_repository = measurement_repository
        self.skill_map = {
            1: "goal keepers",
            2: "defenders",
            3: "midfielders",
            4: "attackers"
        }

    def get_all_player_matches_stats_from_uefa(self) -> list:
        players_matches_dict = {}
        players_data = self.get_all_player_stats_from_uefa()

        start_time = time.time()
        for player in players_data:
            fixtures, stats = self.uefa_repository.get_all_matches_per_player_stats(player['id'])
            player_name = player['name']
            
            if player_name not in players_matches_dict:
                players_matches_dict[player_name] = {'player_name': player_name, 'fixtures': []}

            for match_index in range(len(fixtures)):
                match_id = fixtures[match_index]['mId']
                goals_scored = stats[match_index]['gS']
                assists = stats[match_index]['gA']
                match_date = fixtures[match_index]['dateTime']
                
                players_matches_dict[player_name]['fixtures'].append({
                    'match_id': match_id,
                    'goals_scored': goals_scored,
                    'assists': assists,
                    'date_time': match_date
                })

        end_time = time.time()
        self.measurement_repository.uefa_execution_time = end_time - start_time

        return list(players_matches_dict.values())

    def get_all_player_stats_from_uefa(self) -> list:
        # retrieve players from uefa
        list_of_players = []
        start_time = time.time()
        
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
        
        end_time = time.time()

        self.measurement_repository.uefa_execution_time = end_time - start_time

        return list_of_players