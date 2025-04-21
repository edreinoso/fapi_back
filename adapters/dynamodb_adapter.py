# adapters/dynamodb_adapter.py
import boto3
import time
from datetime import datetime, timezone
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr
from data.ap2 import PlayerTotalScore

class DynamoDBPlayerStatsRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource("dynamodb")
        self.dynamodb_client = boto3.client("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def get_player_stats(self, 
                         player_name: str, 
                         date_condition: str, 
                         attributes: str) -> dict:
        response = self.table.query(
            KeyConditionExpression=Key('PK').eq(f'PLAYER#{player_name}') & Key('SK').begins_with('MATCH#'),
            FilterExpression=Key('match_date').lte(date_condition),  # Only retrieve past matches
            ProjectionExpression=attributes
        )
        return response['Items']
    
    def put_player_point_per_match_ap1(self,
                                       player_name: str,
                                       match_id: str,
                                       player_goals: str,
                                       player_assists: str,
                                       date_time: str) -> str:
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

    def put_player_total_scores_ap2(self, 
                                    player_data: PlayerTotalScore) -> str:
        """Writes a player's total score to DynamoDB."""
        self.table.put_item(
            Item=player_data.to_item()
        )

    def put_measurement_items(self, 
                              execution_method: str, 
                              execution_location: str, 
                              ddb_operation_time: float, 
                              uefa_operation_time: float, 
                              total_operation_time: float, 
                              number_of_players: int, 
                              access_pattern: str, 
                              average_time_per_player: float, 
                              memory_capacity: int): 
        timestamp = datetime.now(timezone.utc).isoformat()        
        self.table.put_item(
            Item={
                'PK': f'{execution_method}#{execution_location}#{access_pattern}#{timestamp}',
                'SK': f'{timestamp}',
                'execution_method': execution_method,
                'execution_location': execution_location,
                'ddb_operation_time': Decimal(str(ddb_operation_time)),
                'uefa_operation_time': Decimal(str(uefa_operation_time)),
                'total_operation_time': Decimal(str(total_operation_time)),
                'average_time_per_player': Decimal(str(average_time_per_player)),
                'access_pattern': access_pattern,
                'number_of_players': number_of_players,
                'memory_capacity': memory_capacity
            }
        )

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