import http.client
import json
import csv
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Skill mapping
skill_map = {
    1: "goal keepers",
    2: "defenders",
    3: "midfielders",
    4: "attackers"
}

def get_uefa_players_data():
    start_time = time.time()
    logging.info("Fetching players data from UEFA.")
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/players/players_80_en_2.json")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    
    cleaned_player_data = []

    for player in data['data']['value']['playerList']:
        # Transform the skill number to its description
        skill_description = skill_map.get(player.get('skill', 0), 'unknown')

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
            'selected by (%)': player.get('selPer', '')
        })
    
    end_time = time.time()
    logging.info(f"UEFA players data fetched and cleaned in {end_time - start_time:.2f} seconds.")
    
    return cleaned_player_data

def csv_table(player_data):
    # Write to a CSV file
    csv_file_path = 'players_data.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'rating', 'value', 'total points', 'goals', 'assist', 'minutes played', 'average points', 'isActive', 'team', 'man of match', 'position', 'goals conceded', 'yellow cards', 'red cards', 'penalties earned', 'balls recovered', 'selected by (%)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in player_data:
            writer.writerow(player)

    print("CSV file created successfully.")

if __name__ == "__main__":
    uefa_players_data  = get_uefa_players_data()
    csv_table(uefa_players_data)
