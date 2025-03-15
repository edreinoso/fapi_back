# application/cli.py
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from core.player_service import PlayerService

# Initialize repository and service
repository = DynamoDBPlayerStatsRepository(table_name="dev-fapi-players-ddb")
player_service = PlayerService(repository)