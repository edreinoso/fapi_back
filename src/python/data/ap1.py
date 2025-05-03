from typing import Dict
from decimal import Decimal
from data.ddb_item import DynamoDBItem

# This class represents a player's match statistics in the DynamoDB table.
# It inherits from the DynamoDBItem class and implements the required methods.
# The constructor initializes the player's attributes based on the provided player dictionary and match details.
# The to_item method converts the player's attributes into a dictionary format suitable for DynamoDB.
# The pk and sk properties define the partition key and sort key for the DynamoDB item.
class PlayerMatchStats(DynamoDBItem):
    def __init__(self, player_name: str, fixture: list, stats: list, points: list, index: int):
        self.player_name = player_name
        self.date_time = fixture[index]['dateTime']
        self.match_id = fixture[index]['mId']
        self.goals_scored = Decimal(str(stats[index]['gS']))
        self.assists = Decimal(str(stats[index]['gA']))
        self.goals_outside_box = Decimal(str(stats[index]['gOB']))
        self.red_cards = Decimal(str(stats[index]['rC']))
        self.yellow_cards = Decimal(str(stats[index]['yC']))
        self.man_of_match = Decimal(str(stats[index]['mOM']))
        self.penalties_earned = Decimal(str(stats[index]['pE']))
        self.points_earned = Decimal(str(points[index]['tPoints']))
        # these attributes below are mostly for defenders and goalkeepers
        # for now I'm going to keep them here, but it would be nice to think
        # about how to use them depending on the position of the player.
        self.goals_conceded = Decimal(str(stats[index]['gC']))
        self.clean_sheet = Decimal(str(stats[index]['cS']))
        self.balls_recovered = Decimal(str(stats[index]['bR']))
        self.saves = Decimal(str(stats[index]['sS']))
        self.penalties_saved = Decimal(str(stats[index]['pS']))

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
            "date_time": self.date_time,
            "goals_outside_box": Decimal(self.goals_outside_box),
            "red_cards": Decimal(self.red_cards),
            "yellow_cards": Decimal(self.yellow_cards),
            "man_of_match": Decimal(self.man_of_match),
            "penalties_earned": Decimal(self.penalties_earned),
            "points_earned": Decimal(self.points_earned),
            "goals_conceded": Decimal(self.goals_conceded),
            "clean_sheet": Decimal(self.clean_sheet),
            "balls_recovered": Decimal(self.balls_recovered),
            "saves": Decimal(self.saves),
            "penalties_saved": Decimal(self.penalties_saved)
        }