# application/cli.py
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from adapters.uefa_adapter import UEFAPlayerStatsRepository
from core.player_service import PlayerService

# Initialize repositories
# players_repository = DynamoDBPlayerStatsRepository(table_name="manual-fapi-ddb")
dev_players_repository = DynamoDBPlayerStatsRepository(table_name="dev-fapi-players-ddb")
manual_players_repository = DynamoDBPlayerStatsRepository(table_name="manual-fapi-ddb")
measurement_repository = DynamoDBPlayerStatsRepository(table_name="dev-fapi-measurement-ddb")
uefa_repository = UEFAPlayerStatsRepository(endpoint_url="/en/uclfantasy/services/feeds/players/players_70_en_9.json")

# Initialize services
player_service = PlayerService(manual_players_repository, uefa_repository)
print('test from cli')