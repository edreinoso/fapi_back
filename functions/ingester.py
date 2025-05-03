import os
import sys
# application/cli.py
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from adapters.uefa_adapter import UEFAPlayerStatsRepository
from core.player_service import PlayerService
from core.uefa_service import UEFAService
from core.measurement_service import MeasurementService

# Read table names from environment variables
players_table_name = os.environ.get("PLAYERS_TABLE_NAME")
measurement_table_name = os.environ.get("MEASUREMENT_TABLE_NAME")

# Initialize repositories
# players_repository = DynamoDBPlayerStatsRepository(table_name="manual-fapi-ddb")
players_repository = DynamoDBPlayerStatsRepository(table_name=players_table_name)
measurement_repository = DynamoDBPlayerStatsRepository(table_name=measurement_table_name)
manual_players_repository = DynamoDBPlayerStatsRepository(table_name="manual-fapi-ddb")
uefa_repository = UEFAPlayerStatsRepository(endpoint_url="/en/uclfantasy/services/feeds/players/players_70_en_9.json")

MEMORY_CAPACITY = 256

# This function will help determine the execution mode and fetch parameters
def get_parameters(event=None) -> tuple[str, str, str]:
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

def ingest(event):
    remove_ddb_table, ap_type, execution_environment = get_parameters(event)
    print(f'{remove_ddb_table} {ap_type} {execution_environment}')
    
    # Initialize services
    measurement_service = MeasurementService(measurement_repository, MEMORY_CAPACITY, execution_environment, 'sequential', ap_type)
    uefa_service = UEFAService(uefa_repository, measurement_service)
    player_service = PlayerService(players_repository, uefa_service, measurement_service)

    # access pattern router
    ap_router = {
        'ap1': lambda: player_service.update_ddb_table_with_ap1(remove_ddb_table), # update player total scores
        'ap2': lambda: player_service.update_ddb_table_with_ap2(remove_ddb_table), # update player total scores
    }

    if ap_type in ap_router:
        ap_router[ap_type]()
    else:
        print(f'Unknown access pattern: {ap_type}')

    # Update dynamodb measurement table
    measurement_service.update_ddb_with_runtime_measurement()

def handler(event, context):
    ingest(event)
    return {
        "statusCode": 200,
        "body": "Success"
    }

if __name__ == "__main__":
    ingest()