# core/ports.py
from typing import Protocol

class PlayerStatsRepository(Protocol):  # Port
    def get_player_stats(self, player_id: str) -> dict:
        """Fetch player statistics by ID"""
        pass