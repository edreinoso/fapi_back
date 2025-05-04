import os
import sys
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from core.player_service import PlayerService

players_table_name = os.environ.get("PLAYERS_TABLE_NAME")

# Initialize repositories
players_repository = DynamoDBPlayerStatsRepository(table_name=players_table_name)

def get_parameters(event=None) -> tuple[str, str]:
    """Determine execution mode and fetch parameters accordingly."""
    if event:
        # Running in Lambda
        player_name = event.get('player_name')
        player_attributes = event.get('player_attributes')
    else:
        # Running local
        if len(sys.argv) < 4:
            print('Usage: uv run <player_name> <player_attributes>')
            sys.exit(1)
        player_name = sys.argv[1]
        player_attributes = sys.argv[2]
    
    return player_name, player_attributes

def fetch(event):
    """Query items in ddb database"""
    # 🌟 Welcoming message
    print("\n⚽ Welcome to the UEFA Fantasy Data Explorer! ⚽")
    print("You can retrieve stats for any player!\n")

    player_name, player_attributes = get_parameters(event)
    print(f'Player name: {player_name}, Player attribute: {player_attributes}')

    # Initialize services
    player_service = PlayerService(players_repository, uefa_service=None, measurement=None)
    return player_service.get_player_stats_from_ddb(player_name, player_attributes)


def handler(event, context):
    """AWS Lambda handler function."""
    player_data = fetch(event)
    return {
        'statusCode': 200,
        'body': player_data
    }

if __name__ == "__main__":
    fetch()
    