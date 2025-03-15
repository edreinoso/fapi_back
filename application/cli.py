# application/cli.py
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from core.player_service import PlayerService

# Initialize repository and service
repository = DynamoDBPlayerStatsRepository(table_name="player_stats")
player_service = PlayerService(repository)