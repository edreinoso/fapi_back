# main.py
from application.cli import player_service

if __name__ == "__main__":
    player_id = "1234"
    print(player_service.get_player_performance(player_id))