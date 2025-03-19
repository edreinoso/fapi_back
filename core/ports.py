# core/ports.py
from typing import Protocol

class DDBPlayerStatsRepository(Protocol):  # Port
    def get_player_stats(self, player_name: str, date_condition: str, attributes: str) -> dict:
        """Fetch player statistics by ID"""
        pass

    # Access Pattern 1
    def put_player_point_per_match_ap1(self,
                                       player_name: str,
                                       match_id: str,
                                       player_goals: str,
                                       player_assists: str,
                                       date_time: str) -> str:
        """Update player point per match"""
        pass

    # Access Pattern 2
    def put_player_total_scores_ap2(self, 
                               player_name: str, 
                               player_id: str, 
                               player_goals: str, 
                               player_assists: str, 
                               team: str, 
                               position: str) -> str:
        """Update player total score"""
        pass

    # Access Pattern 3
    def put_matches_stats_ap3(self, 
                         player_name: str, 
                         match_id: str, 
                         player_goals: str, 
                         player_assists: str, 
                         date_time: str) -> str:
        """Update match player"""
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

class UEFAPlayerStatsRepository(Protocol):
    def get_all_matches_per_player_stats(self, player_id: str) -> dict:
        """Fetch all matches per player statistics"""
        pass
    
    def get_all_player_stats(self) -> dict:
        """Fetch all player statistics"""
        pass