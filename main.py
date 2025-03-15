# main.py
from application.cli import player_service

if __name__ == "__main__":
    player_name = "pedri"
    attributes = "goals, match_date"
    print(player_service.get_player_performance(player_name, attributes))