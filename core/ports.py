# core/ports.py
from typing import Protocol

class PlayerStatsRepository(Protocol):  # Port
    def get_player_stats(self, player_name: str, date_condition: str, attributes: str) -> dict:
        """Fetch player statistics by ID"""
        pass