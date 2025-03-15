# core/player_service.py
from core.ports import DDBPlayerStatsRepository
from datetime import datetime, timezone

class PlayerService:
    def __init__(self, stats_repository: DDBPlayerStatsRepository, uefa_repository: UEFAPlayerStatsRepository):
        self.stats_repository = stats_repository

        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')  # Get today's date in YYYY-MM-DD format
        stats = self.stats_repository.get_player_stats(player_name, today, attributes)
        if not stats:
            return {"error": "Player not found"}

        return stats