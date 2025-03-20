# core/player_service.py
import time
from core.ports import DDBPlayerStatsRepository
from core.measurement_service import MeasurementService
from datetime import datetime, timezone


class PlayerService:
    def __init__(self, stats_repository: DDBPlayerStatsRepository, uefa_repository: UEFAPlayerStatsRepository, measurement: MeasurementService):
        self.uefa_repository = uefa_repository
        self.ddb_repository = ddb_repository
        self.measurement = measurement
        
    def recreate_ddb_table(self) -> str:
        self.ddb_repository.delete_table()
        self.ddb_repository.describe_table()
        self.ddb_repository.create_table()
        return "Table has been recreated"
    
    def transform_date(self, source_date):
        return datetime.strptime(source_date, "%m/%d/%y %I:%M:%S %p").strftime("%Y-%m-%d")

    def update_ddb_table_with_ap1_and_ap3(self, ap: str) -> str:
        print('test from player_service (update_ddb_table_with_ap1)')
        
        # get all players from uefa
        total_execution_start_time = time.time()
        uefa_start_time = time.time()
        list_of_players = self.get_all_player_stats_from_uefa()
        uefa_end_time = time.time()

        ddb_start_time = time.time()
        # update player matches in ddb
        for player in list_of_players:
            fixtures, stats = self.uefa_repository.get_all_matches_per_player_stats(player['id'])

            for matches in range(0,len(fixtures)):
                match_id = fixtures[matches]['mId']
                goals_scored = stats[matches]['gS']
                assists = stats[matches]['gA']
                match_date = self.transform_date(fixtures[matches]['dateTime'])

                if ap == 'ap1':
                    self.ddb_repository.put_player_point_per_match_ap1(player['name'], match_id, goals_scored, assists, match_date)
                elif ap == 'ap3':
                    self.ddb_repository.put_matches_stats_ap3(player['name'], match_id, goals_scored, assists, player['position'], match_date)

        ddb_end_time = time.time()
        total_execution_end_time = time.time()
        
        self.measurement.number_of_players = len(list_of_players)
        self.measurement.average_time_per_player = (ddb_end_time - ddb_start_time) / len(list_of_players)
        self.measurement.uefa_execution_time = uefa_end_time - uefa_start_time
        self.measurement.ddb_execution_time = ddb_end_time - ddb_start_time
        self.measurement.total_execution_time = total_execution_end_time - total_execution_start_time

    def update_ddb_table_with_ap2(self, remove_ddb_table: str) -> str:
        # 1️⃣ delete ddb table
        if remove_ddb_table == 'y':
            self.recreate_ddb_table()
            time.sleep(10)
        
        # 2️⃣ get all players from uefa
        total_execution_start_time = time.time()
        uefa_start_time = time.time()
        list_of_players = self.get_all_player_stats_from_uefa()
        uefa_end_time = time.time()

        # 3️⃣ update players in fapi ddb
        ddb_start_time = time.time()
        for player in list_of_players:
            self.ddb_repository.put_player_total_scores_ap2(player['name'], player['id'], player['goals'], player['assist'], player['team'], player['position'])
        ddb_end_time = time.time()
        total_execution_end_time = time.time()

        self.measurement.number_of_players = len(list_of_players)
        self.measurement.average_time_per_player = (ddb_end_time - ddb_start_time) / len(list_of_players)
        self.measurement.uefa_execution_time = uefa_end_time - uefa_start_time
        self.measurement.ddb_execution_time = ddb_end_time - ddb_start_time
        self.measurement.total_execution_time = total_execution_end_time - total_execution_start_time

        return "All players with access pattern two have been updated"

    def get_player_stats_from_ddb(self, player_name: str, attributes: str) -> dict:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
        stats = self.ddb_repository.get_player_stats(player_name, today, attributes)
        if not stats:
            return {"error": "Player not found"}

        return stats