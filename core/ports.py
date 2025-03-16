# core/ports.py
from typing import Protocol

class DDBPlayerStatsRepository(Protocol):  # Port
    def get_player_stats(self, player_name: str, date_condition: str, attributes: str) -> dict:
        """Fetch player statistics by ID"""
        pass

    # Access Pattern 2
    def put_player_total_score(self, player_name: str, player_id: str, player_goals: str, player_assists: str, team: str, position: str) -> str:
        """Update player total score"""
        pass

    def create_table(self, table_name: str):
        """Create a DynamoDB table"""
        pass

    def delete_table(self, table_name: str):
        """Delete a DynamoDB table"""
        pass

class UEFAPlayerStatsRepository(Protocol):
    def get_all_player_stats(self) -> dict:
        """Fetch all player statistics"""
        pass