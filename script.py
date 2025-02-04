import http.client
import json
import csv
import boto3
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


if __name__ == "__main__":
    players_data  = get_players_data() # list of players
    csv_table(players_data)
    write_to_ddb(players_data) # write data to ddb
    