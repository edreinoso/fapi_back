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

# Headers
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_players_data():
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/players/players_70_en_6.json")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    
    cleaned_player_data = []

    for player in data['data']['value']['playerList']:
        # Transform the skill number to its description
        skill_description = skill_map.get(data.get('skill', 0), 'unknown')

        cleaned_player_data.append({
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

    return cleaned_player_data

def csv_table(player_data):
    # Write to a CSV file
    csv_file_path = 'players3.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'value', 'total points', 'goals', 'assist', 'minutes played', 'average points', 'isActive', 'team', 'man of match', 'position', 'goals conceded', 'yellow cards', 'red cards', 'penalties earned', 'balls recovered']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in player_data:
            writer.writerow(player)

    print("CSV file created successfully.")

def get_notion_existing_entries():
    all_entries = []
    has_more = True
    next_cursor = None

    while has_more:
        payload = {"start_cursor": next_cursor} if next_cursor else {}
        response = requests.post(NOTION_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            all_entries.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor", None)
        else:
            print("Failed to fetch entries:", response.text)
            break

    # Extract the relevant data
    existing_entries = {
        entry["properties"]["name"]["title"][0]["text"]["content"]: entry["id"]
        for entry in all_entries
    }

    return existing_entries

if __name__ == "__main__":
    players_data  = get_players_data()
    csv_table(players_data['data']['value']['playerList'])
    notion()
        existing_entries = get_notion_existing_entries()
    existing_entries = get_notion_existing_entries()
