import http.client
import json
import csv
# from notion import Notion

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

if __name__ == "__main__":
    players_data  = get_players_data()
    csv_table(players_data['data']['value']['playerList'])
    
    # notion_db = Notion(notion_token, notion_database_id)
    
    count = 0

    """for player in players_data['data']['value']['playerList']:
        count += 1
        
        skill_description = skill_map.get(player.get('skill', 0), 'unknown')

        properties = {
            'name':{'title': [{'text': {'content': player.get('pDName', '')}}]},
            'rating':{'title': [{'text': {'content': player.get('rating', '')}}]},
            'value':{'title': [{'text': {'content': player.get('value', '')}}]},
            'total_points':{'title': [{'text': {'content': player.get('totPts', '')}}]},
            'goals':{'title': [{'text': {'content': player.get('gS', '')}}]},
            'assist':{'title': [{'text': {'content': player.get('assist', '')}}]},
            'minutes_played':{'title': [{'text': {'content': player.get('minsPlyd', '')}}]},
            'average_points':{'title': [{'text': {'content': player.get('avgPlayerPts', '')}}]},
            'isActive':{'title': [{'text': {'content': player.get('isActive', '')}}]},
            'team':{'title': [{'text': {'content': player.get('cCode', '')}}]},
            'man_of_match':{'title': [{'text': {'content': player.get('mOM', '')}}]},
            'position':{'title': [{'text': {'content': skill_description}}]},
            'goals_conceded':{'title': [{'text': {'content': player.get('yC')}}]},
            'yellow_cards':{'title': [{'text': {'content': player.get('rC')}}]},
            'red_cards':{'title': [{'text': {'content': player.get('pE')}}]},
            'penalties_earned':{'title': [{'text': {'content': player.get('bR')}}]},
            'balls_recovered':{'title': [{'text': {'content':  player.get('bR')}}]}
        }

        print(properties)"""

        # notion_db.write_row(properties)
    
    name = 'helloworld'
    # notion_db.write_row(name)
    # print(count)
    