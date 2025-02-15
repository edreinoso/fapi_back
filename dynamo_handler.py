import boto3
from boto3.dynamodb.conditions import Key, Attr

class DynamoDBHandler:
    def __init__(self, table_name: str):
        """Initialize with a specific DynamoDB table."""
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table(table_name)

    def write_player_total_score(self, player_name, player_id, player_goals, player_assists, team, position):
        """Writes a player's total score to DynamoDB."""
        self.table.put_item(
            Item={
                'PK': f'PLAYER#{player_name}',
                'SK': 'TOTALS',
                'player_id': player_id,
                'goals': player_goals,
                'assists': player_assists,
                'team': team,
                'position': position
            }
        )

    def write_match_player(self, player_name, match_id, player_goals, player_assists, date_time):
        """Writes an individual player's match stats."""
        self.table.put_item(
            Item={
                'PK': f'PLAYER#{player_name}',
                'SK': f'MATCH#{date_time}#{match_id}',
                'match_id': match_id,
                'goals': player_goals,
                'assists': player_assists,
                'match_date': date_time
            }
        )

    def write_match_data(self, player_name, match_id, player_goals, player_assists, position, date_time):
        """Writes match data including position info."""
        self.table.put_item(
            Item={
                'PK': f'MATCH#{date_time}#{match_id}',
                'SK': f'PLAYER#{player_name}',
                'match_id': match_id,
                'goals': player_goals,
                'assists': player_assists,
                'position': position,
                'match_date': date_time
            }
        )
    
    def query_player_data(self, player_name, attributes, date_condition):
        """Query DynamoDB for a player's data."""
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f'PLAYER#{player_name}') & Key('SK').begins_with('MATCH#'),
            FilterExpression=Key('match_date').lt(date_condition),  # Only retrieve past matches
            ProjectionExpression=attributes
        )
        return response['Items']