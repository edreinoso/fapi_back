# adapters/dynamodb_adapter.py
import boto3

class DynamoDBPlayerStatsRepository:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def get_player_stats(self, player_id: str) -> dict:
        response = self.table.get_item(Key={"player_id": player_id})
        return response.get("Item", {})