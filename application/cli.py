import sys
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

def get_parameters(event=None):
    """Determine execution mode and fetch parameters accordingly."""
    if event:
        # Running in Lambda
        remove_ddb_table = event.get('ddb_recreate')
        ap_type = event.get('ap_type')
        execution_environment = event.get('execution_environment')
    else:
        # Running local
        if len(sys.argv) < 4:
            print('Usage: uv run <ddb_recreate> <ap_type> <execution_environment>')
            sys.exit(1)
        remove_ddb_table = sys.argv[1]
        ap_type = sys.argv[2]
        execution_environment = sys.argv[3]
    
    return remove_ddb_table, ap_type, execution_environment

def main():
    remove_ddb_table, ap_type, execution_environment = get_parameters()
    print(f'{remove_ddb_table} {ap_type} {execution_environment}')