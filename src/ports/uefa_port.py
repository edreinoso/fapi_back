# core/uefa_port.py
from typing import Protocol

class UEFAPlayerStatsRepository(Protocol):
    def get_all_matches_per_player_stats(self, player_id: str) -> dict:
        """Fetch all matches per player statistics"""
        pass
    
    def get_all_player_stats(self) -> dict:
        """Fetch all player statistics"""
        pass