from typing import Dict
from decimal import Decimal
from data.ddb_item import DynamoDBItem

# This class represents a player's total score in the DynamoDB table.
# It inherits from the DynamoDBItem class and implements the required methods.
# The constructor initializes the player's attributes based on the provided player dictionary and skill description.
# The to_item method converts the player's attributes into a dictionary format suitable for DynamoDB.
# The pk and sk properties define the partition key and sort key for the DynamoDB item.
class PlayerTotalScore(DynamoDBItem):
    def __init__(self, player: dict, skill_description: str):
        self.id = player.get('id', '')
        self.name = player.get('pDName', '')
        self.team = player.get('cCode', '')
        self.position = skill_description
        self.rating = Decimal(str(player.get('rating', 0)))
        self.value = Decimal(str(player.get('value', 0)))
        self.total_points = Decimal(str(player.get('totPts', 0)))
        self.goals = Decimal(str(player.get('gS', 0)))
        self.assist = Decimal(str(player.get('assist', 0)))
        self.minutes_played = Decimal(str(player.get('minsPlyd', 0)))
        self.average_points = Decimal(str(player.get('avgPlayerPts', 0)))
        self.is_active = Decimal(str(player.get('isActive', 0)))
        self.man_of_match = Decimal(str(player.get('mOM', 0)))
        self.goals_conceded = Decimal(str(player.get('gC', 0)))
        self.yellow_cards = Decimal(str(player.get('yC', 0)))
        self.red_cards = Decimal(str(player.get('rC', 0)))
        self.penalties_earned = Decimal(str(player.get('pE', 0)))
        self.balls_recovered = Decimal(str(player.get('bR', 0)))

    @property
    def pk(self) -> str:
        return f"PLAYER#{self.name.lower()}"

    @property
    def sk(self) -> str:
        return "TOTALS"

    def to_item(self) -> Dict[str, str]:
        return {
            **self.keys(),
            "player_id": self.id,
            "rating": self.rating,
            "value": self.value,
            "total_points": self.total_points,
            "goals": self.goals,
            "assist": self.assist,
            "minutes_played": self.minutes_played,
            "average_points": self.average_points,
            "is_active": self.is_active,
            "team": self.team,
            "man_of_match": self.man_of_match,
            "position": self.position,
            "goals_conceded": self.goals_conceded,
            "yellow_cards": self.yellow_cards,
            "red_cards": self.red_cards,
            "penalties_earned": self.penalties_earned,
            "balls_recovered": self.balls_recovered,
        }