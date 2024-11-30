import http.client
import requests
import json
import csv

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

def get_players_data() -> dict:
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/players/players_70_en_6.json")
    res = conn.getresponse()
    data = res.read()
    players_data = json.loads(data.decode("utf-8"))
    return players_data

def csv_table(players):
    player_data = []

    for player in players:
        # Transform the skill number to its description
        skill_description = skill_map.get(player.get('skill', 0), 'unknown')

        player_data.append({
            'name': player.get('pDName', ''),
            'rating': player.get('rating', ''),
            'value': player.get('value', ''),
            'total points': player.get('totPts', ''),
            'goals': player.get('gS', ''),
            'assist': player.get('assist', ''),
            'minutes played': player.get('minsPlyd', ''),
            'average points': player.get('avgPlayerPts', ''),
            'isActive': player.get('isActive', ''),
            'team': player.get('cCode', ''),
            'man of match': player.get('mOM', ''),
            'position': skill_description,
            'goals conceded': player.get('gC'),
            'yellow cards': player.get('yC'),
            'red cards': player.get('rC'),
            'penalties earned': player.get('pE'),
            'balls recovered': player.get('bR'),
        })

    # Write to a CSV file
    csv_file_path = 'players3.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'value', 'total points', 'goals', 'assist', 'minutes played', 'average points', 'isActive', 'team', 'man of match', 'position', 'goals conceded', 'yellow cards', 'red cards', 'penalties earned', 'balls recovered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in player_data:
            writer.writerow(player)

    print("CSV file created successfully.")

def notion():
    # Headers
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    response = requests.post(NOTION_API_URL, headers=headers)
    notion_data = response.json()

    print(notion_data)

    return

    # Extract the relevant data
    existing_entries = {
        entry["properties"]["name"]["title"][0]["text"]["content"]: entry["id"]
        for entry in notion_data["results"]
    }

    print(existing_entries)

if __name__ == "__main__":
    players_data  = get_players_data()
    csv_table(players_data['data']['value']['playerList'])
    notion()
    