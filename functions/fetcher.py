import os
import sys
from adapters.dynamodb_adapter import DynamoDBPlayerStatsRepository
from core.player_service import PlayerService

players_table_name = os.environ.get("PLAYERS_TABLE_NAME")

# Initialize repositories
players_repository = DynamoDBPlayerStatsRepository(table_name=players_table_name)

def fetch(event):
    """Query items in ddb database"""
    # 🌟 Welcoming message
    print("\n⚽ Welcome to the UEFA Fantasy Data Explorer! ⚽")
    print("You can retrieve stats for any player!\n")

    player_name = event['player_name']
    player_attributes = event['player_attributes']
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
    