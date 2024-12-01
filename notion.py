
class Notion:
    def __init__(self, requests):
        self.request = requests
        self.database_id = NOTION_DATBASE_ID
        self.token = NOTION_TOKEN
        self.api = NOTION_API_URL
        self.headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def get_notion_existing_entries(self):
        all_entries = []
        has_more = True
        next_cursor = None

        while has_more:
            payload = {"start_cursor": next_cursor} if next_cursor else {}
            response = self.requests.post(NOTION_API_URL, headers=self.headers, json=payload)
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
    
    def update_notion_entries(self, players_data, existing_entries):
        # print(existing_entries)
        for player in players_data:
            player_name = player["name"]
            if player_name in existing_entries:
                page_id = existing_entries[player_name]

                # Prepare update payload
                data = {
                    "properties": {
                        "name": {"title": [{"text": {"content": player["name"]}}]},
                        "rating": {"number": player["rating"]},
                        "value": {"number": player["value"]},
                        "total points": {"number": player["total points"]},
                        "goals": {"number": player["goals"]},
                        "assist": {"number": player["assist"]},
                        "minutes played": {"number": player["minutes played"]},
                        "average points": {"number": player["average points"]},
                        "isActive": {"number": player["isActive"]},
                        "team": {"select": {"name": player["team"]}},
                        "man of match": {"number": player["man of match"]},
                        "position": {"select": {"name": player["position"]}},
                        "goals conceded": {"number": player["goals conceded"]},
                        "yellow cards": {"number": player["yellow cards"]},
                        "red cards": {"number": player["red cards"]},
                        "penalties earned": {"number": player["penalties earned"]},
                        "balls recovered": {"number": player["balls recovered"]},
                    }
                }

                print(data,page_id)

                # Send the PATCH request
                # response = self.requests.patch(
                #     f"https://api.notion.com/v1/pages/{page_id}",
                #     headers=self.headers,
                #     json=data
                # )

                # if response.status_code == 200:
                #     print(f"Updated {player_name} successfully!")
                # else:
                #     print(f"Failed to update {player_name}: {response.text}")