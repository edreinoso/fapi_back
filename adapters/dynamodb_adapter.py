# adapters/dynamodb_adapter.py
import time
from boto3.dynamodb.conditions import Key, Attr
import boto3

class DynamoDBPlayerStatsRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def get_player_stats(self, player_name: str, date_condition: str, attributes: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f'PLAYER#{player_name}') & Key('SK').begins_with('MATCH#'),
            FilterExpression=Key('match_date').lte(date_condition),  # Only retrieve past matches
            ProjectionExpression=attributes
        )
        return response['Items']
    
    def put_player_point_per_match_ap1(self):
        pass

    def put_player_total_scores_ap2(self, player_name: str, player_id: str, goals: str, assists: str, team: str, position: str) -> str:
        """Writes a player's total score to DynamoDB."""
        self.table.put_item(
            Item={
                'PK': f'PLAYER#{player_name}',
                'SK': 'TOTALS',
                'player_id': player_id,
                'goals': goals,
                'assists': assists,
                'team': team,
                'position': position
            }
        )

    def put_matches_stats_ap3(self):
        pass

    def create_table(self):
        self.dynamodb_client.create_table(
            TableName=self.table_name,
            KeySchema=[{'AttributeName': 'PK', 'KeyType': 'HASH'}, {'AttributeName': 'SK', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{'AttributeName': 'PK', 'AttributeType': 'S'}, {'AttributeName': 'SK', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"Table {self.table_name} has been recreated.")
    
    def delete_table(self) -> str:
        try:
            self.dynamodb_client.delete_table(TableName=self.table_name)
            print(f"Table {self.table_name} has been deleted.")
            time.sleep(5)
        except self.dynamodb_client.exceptions.ResourceNotFoundException:
            print(f'Table {self.table_name} does not exist.')

    def describe_table(self):
        while True:
            try:
                self.dynamodb_client.describe_table(TableName=self.table_name)
                time.sleep(5)
            except self.dynamodb_client.exceptions.ResourceNotFoundException:
                break  # Table is fully deleted