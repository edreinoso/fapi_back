# core/player_service.py
from core.ports import PlayerStatsRepository
from datetime import datetime, timezone

class PlayerService:
    def __init__(self, stats_repository: PlayerStatsRepository):
        self.stats_repository = stats_repository

    def get_player_performance(self, player_name: str, attributes: str) -> dict:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
        stats = self.stats_repository.get_player_stats(player_name, today, attributes)
        if not stats:
            return {"error": "Player not found"}

        # Business logic: Calculate fantasy points
        fantasy_points = (stats["goals"] * 4) + (stats["assists"] * 3) + (stats["recoveries"] * 1)
        return {
            "player_id": player_id,
            "goals": stats["goals"],
            "assists": stats["assists"],
            "recoveries": stats["recoveries"],
            "fantasy_points": fantasy_points,
        }