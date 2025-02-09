import http.client
import json
import csv
from dynamo_handler import DynamoDBHandler
import matplotlib.pyplot as plt
import numpy as np
# from notion import Notion

# Initialize the handler
ddb_handler = DynamoDBHandler('manual-fapi-ddb')

notion_token = ''
notion_page_id = ''
notion_database_id = ''

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

        if player.get('pDName', '') == 'K. Mbappé':
            list_of_players.append({
                'id': player.get('id', ''),
                'name': player.get('pDName', ''),
                'goals': player.get('gS', ''),
                'assist': player.get('assist', ''),
                'team': player.get('cCode', ''),
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

def get_individual_match_player_data(player_data):
    print(player_data)
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
            
            print(f'{player['name']} facts - match id: {match_id}, goals: {goals_scored}, assists: {assists}, dateTime: {match_date}')
            
            ddb_handler.write_match_player(player['name'], match_id, goals_scored, assists, match_date)
            ddb_handler.write_match_data(player['name'], match_id, goals_scored, assists, player['position'], match_date)

def visualize_data_in_matplotlib(player_stats: list, player_name: str):
    # Extracting the goals
    goals = [int(d['goals']) for d in player_stats]

    # Match numbers (assuming matches are in order)
    matches = np.arange(1, len(goals) + 1)

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(matches, goals, marker='o', linestyle='-', color='b', label="Goals per match")
    plt.xlabel("Match Number")
    plt.ylabel("Goals")
    plt.title(f"{player_name} Goals Per Match")
    plt.xticks(matches)  # Ensure each match is labeled
    plt.yticks(range(max(goals) + 1))  # Show all goal count possibilities
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()

def read_player_from_ddb(player):
    pass

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

if __name__ == "__main__":
    """Put items in ddb database"""
    players_data  = get_players_data() # list of players
    store_player_in_ddb(players_data)
    get_individual_match_player_data(players_data)
    
    """Query items in ddb database"""
    # 🌟 Welcoming message
    print("\n⚽ Welcome to the UEFA Fantasy Data Explorer! ⚽")
    print("You can retrieve stats for any player!\n")

    # 📝 User input for player name and attribute
    player_name = input("Enter the player's name: ").strip()
    attribute = input("Enter the attribute to retrieve (e.g., goals, assists, points): ").strip()

    player_stats = ddb_handler.query_player_data(player_name, attribute)
    print(player_stats)
    visualize_data_in_matplotlib(player_stats, player_name)
