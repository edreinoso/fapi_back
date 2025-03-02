import logging
import http.client
import json
import csv
import time
from datetime import datetime, timezone
from dynamo_handler import DynamoDBHandler

# Initialize the handler
ddb_handler = DynamoDBHandler('manual-fapi-ddb')

# Skill mapping
skill_map = {
    1: "goal keepers",
    2: "defenders",
    3: "midfielders",
    4: "attackers"
}

def transform_players_data(players_data: dict) -> list:
    list_of_players = []

    for player in players_data:
        # Transform the skill number to its description
        skill_description = skill_map.get(player.get('skill', 0), 'unknown')

        if player.get('pDName', '') == 'K. Mbappé' or player.get('pDName', '') == 'Rodrygo':
            list_of_players.append({
                'id': player.get('id', ''),
                'name': player.get('pDName', '').lower(),
                'goals': player.get('gS', ''),
                'assist': player.get('assist', ''),
                'team': player.get('tName', ''),
                'position': skill_description
            })

    return list_of_players

def get_players_data() -> list:
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/players/players_70_en_9.json")
    res = conn.getresponse()
    data = res.read()
    players_data = json.loads(data.decode("utf-8"))
    list_of_players = transform_players_data(players_data['data']['value']['playerList'])
    return list_of_players

def csv_table(list_of_players):
    # Write to a CSV file
    csv_file_path = 'mbappe.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'id', 'total points', 'goals', 'assist', 'team']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in list_of_players:
            writer.writerow(player)

    print("CSV file created successfully.")

def transform_date(source_date):
    return datetime.strptime(source_date, "%m/%d/%y %I:%M:%S %p").strftime("%Y-%m-%d")

    print(player_data)
def process_match_data_for_players(player_data, access_pattern):
    for player in player_data:
        conn = http.client.HTTPSConnection("gaming.uefa.com")
        conn.request("GET", f"/en/uclfantasy/services/feeds/popupstats/popupstats_70_{player['id']}.json")
        res = conn.getresponse()
        data = res.read()
        players_data_per_match = json.loads(data.decode("utf-8"))
        fixtures = players_data_per_match['data']['value']['fixtures']
        stats = players_data_per_match['data']['value']['stats']

        for matches in range(0,len(fixtures)):
            match_id = fixtures[matches]['mId']
            goals_scored = stats[matches]['gS']
            assists = stats[matches]['gA']
            match_date = transform_date(fixtures[matches]['dateTime'])

            if access_pattern == 'AP1':
                ddb_handler.write_match_player(player['name'], match_id, goals_scored, assists, match_date)
            elif access_pattern == 'AP3':
                ddb_handler.write_match_data(player['name'], match_id, goals_scored, assists, player['position'], match_date)

def store_player_in_ddb(players: list):
    """Writes transformed player data to DynamoDB."""
    for player in players:
        ddb_handler.write_player_total_score(
            player['name'], 
            player['id'], 
            player['goals'], 
            player['assist'], 
            player['team'], 
            player['position']
        )

def main():
    if remove_ddb_table == "y":
        ddb_handler.recreate_table('manual-fapi-ddb')
        time.sleep(10)
    
    """Put items in ddb database"""
    ingester_start_time = time.time()
    uefa_start_time = time.time()
    players_data  = get_players_data() # list of players
    uefa_end_time = time.time()
    uefa_execution_time = uefa_end_time - uefa_start_time
    
    # Routing logic (switch-like behavior)
    ap_router = {
        "AP1": lambda: process_match_data_for_players(players_data, access_pattern="AP1"),
        "AP2": lambda: store_player_in_ddb(players_data),
        "AP3": lambda: process_match_data_for_players(players_data, access_pattern="AP3"),
    }

    ap_type = "AP3"

    if ap_type in ap_router:
        ap_router[ap_type]()
    else:
        print(f"Unknown access pattern: {ap_type}")

    ingester_end_time = time.time()
    total_execution_time = ingester_end_time - ingester_start_time
    ddb_execution_time = total_execution_time - uefa_execution_time
    average_time_per_player = ddb_execution_time / len(players_data)
    
    logging.info(f"Total execution time: {total_execution_time} seconds")
    print(f"Players recorded: {len(players_data)}")
    print(f"Uefa execution time: {uefa_execution_time:.2f} seconds.\nDynamoDB execution time: {ddb_execution_time:.2f} seconds. \nTotal execution time: {total_execution_time:.2f} seconds.\nAverage time per player: {average_time_per_player:.2f} seconds.")
    
def handler(event, context): 
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
