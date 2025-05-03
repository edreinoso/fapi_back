# core/ddb_port.py
from typing import Protocol
from data.ap2 import PlayerTotalScore
from data.ap1 import PlayerMatchStats

class DDBPlayerStatsRepository(Protocol):  # Port
    def get_player_stats(self, 
                         player_name: str, 
                         date_condition: str, 
                         attributes: str) -> dict:
        """Fetch player statistics by ID"""
        pass

    # Access Pattern 1
    def put_player_point_per_match_ap1(self,
                                       player_data: PlayerMatchStats) -> str:
        """Update player point per match"""
        pass

    # Access Pattern 2
    def put_player_total_scores_ap2(self, 
                               player_data: PlayerTotalScore) -> str:
        """Update player total score"""
        pass

    def create_table(self, table_name: str):
        """Create a DynamoDB table"""
        pass

    def delete_table(self, table_name: str):
        """Delete a DynamoDB table"""
        pass

    def describe_table(self, table_name: str):
        """Describe a DynamoDB table"""
        pass

    def put_measurement_items(self,
                              execution_method: str,
                              execution_location: str,
                              ddb_operation_time: float,
                              uefa_operation_time: float,
                              total_operation_time: float,
                              number_of_players: int,
                              access_pattern: str,
                              average_time_per_player: float,
                              memory_capacity: int):
        """Put measurement items"""
        pass
