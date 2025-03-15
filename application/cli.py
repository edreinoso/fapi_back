# application/cli.py
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from core.player_service import PlayerService

# Initialize repository and service
player_service = PlayerService(repository)players_repository = DynamoDBPlayerStatsRepository(table_name="dev-fapi-players-ddb")
measurement_repository = DynamoDBPlayerStatsRepository(table_name="dev-fapi-measurement-ddb")
