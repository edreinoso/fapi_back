# adapters/dynamodb_adapter.py
import time
from boto3.dynamodb.conditions import Key, Attr
import boto3

class DynamoDBPlayerStatsRepository:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def get_player_stats(self, player_name: str, date_condition: str, attributes: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f'PLAYER#{player_name}') & Key('SK').begins_with('MATCH#'),
            FilterExpression=Key('match_date').lte(date_condition),  # Only retrieve past matches
            ProjectionExpression=attributes
        )
        return response['Items']