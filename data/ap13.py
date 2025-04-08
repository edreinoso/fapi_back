from typing import Dict
from decimal import Decimal
from data.ddb_item import DynamoDBItem

# This class represents a player's match statistics in the DynamoDB table.
# It inherits from the DynamoDBItem class and implements the required methods.
# The constructor initializes the player's attributes based on the provided player dictionary and match details.
# The to_item method converts the player's attributes into a dictionary format suitable for DynamoDB.
# The pk and sk properties define the partition key and sort key for the DynamoDB item.
class PlayerMatchStats(DynamoDBItem):
    def __init__(self, player: dict, match_id: str, goals_scored: str, assists: str, date_time: str):
        self.player_name = player.get('player_name', '')
        self.match_id = match_id
        self.goals_scored = goals_scored
        self.assists = assists
        self.date_time = date_time

    @property
    def pk(self) -> str:
        return f"PLAYER#{self.player_name.lower()}"

    @property
    def sk(self) -> str:
        return f"MATCH#{self.date_time}#{self.match_id}"
    
    def to_item(self) -> Dict[str, str]:
        return {
            **self.keys(),
            "match_id": self.match_id,
            "goals_scored": Decimal(self.goals_scored),
            "assists": Decimal(self.assists),
            "date_time": self.date_time
        }