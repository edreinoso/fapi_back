# main.py
from application.cli import player_service

if __name__ == "__main__":
    player_name = "pedri"
    attributes = "goals, match_date"
    print(player_service.get_player_stats_from_ddb(player_name, attributes))
    print(player_service.get_all_player_stats_from_uefa())