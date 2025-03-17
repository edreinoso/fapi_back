# main.py
from application.cli import player_service

def handler(event, context):
    main(event)
    return {
        "statusCode": 200,
        "body": "Success"
    }

if __name__ == "__main__":
    player_name = "pedri"
    attributes = "goals, match_date"
    # print(player_service.get_player_stats_from_ddb(player_name, attributes))
    print(player_service.update_ddb_table_with_latest_player_data())