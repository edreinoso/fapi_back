import time
from core.ports import UEFAPlayerStatsRepository
from core.measurement_service import MeasurementService
from data.ap2 import PlayerTotalScore
from data.ap1 import PlayerMatchStats

class UEFAService:
    def __init__(self, uefa_repository: UEFAPlayerStatsRepository, measurement: MeasurementService): 
        self.uefa_repository = uefa_repository
        self.measurement = measurement
        self.skill_map = {
            1: "goal keepers",
            2: "defenders",
            3: "midfielders",
            4: "attackers"
        }

    def get_all_player_matches_stats_from_uefa(self) -> list:
        print("Retrieving all matches for players from UEFA...")
        start_time = time.time()
        
        players_matches_dict = {}
        players_data = self.get_all_player_stats_from_uefa()

        for player in players_data:
            fixtures, stats, points = self.uefa_repository.get_all_matches_per_player_stats(player.id)
            player_name = player.name
            player_position = player.position
            player_id = player.id
            
            players_matches_dict[player_id] = {'player_id': player_id, 'fixtures': []}
            players_matches_dict[player_id]['player_name'] = player_name
            players_matches_dict[player_id]['position'] = player_position

            for match_index in range(len(fixtures)):
                player_match_stats = PlayerMatchStats(player_name, fixtures, stats, points, match_index)
                players_matches_dict[player_id]['fixtures'].append(player_match_stats)

        end_time = time.time()

        self.measurement.increment_uefa_execution_time(end_time - start_time)

        print('Finished retrieving all matches for the players from UEFA')

        return list(players_matches_dict.values())

    def get_all_player_stats_from_uefa(self) -> list:
        print("\nRetrieving all players from UEFA...")
        start_time = time.time()

        list_of_players = []
        
        # retrieve players from uefa
        players_data = self.uefa_repository.get_all_player_stats()

        for player in players_data:
            # Transform the skill number to its description
            # if player.get('pDName') == 'Pedri': # this statement should be used as test
            skill_description = self.skill_map.get(player.get('skill', 0), 'unknown')
            player_total_score = PlayerTotalScore(player, skill_description)
            list_of_players.append(player_total_score)
                      
        end_time = time.time()

        self.measurement.increment_uefa_execution_time(end_time - start_time)

        print('Finished retrieving all players from UEFA')

        return list_of_players