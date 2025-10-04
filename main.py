import csv
import http.client
import json
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Skill mapping
skill_map = {1: "goal keepers", 2: "defenders", 3: "midfielders", 4: "attackers"}

# Team name mapping - API names to standardized names
team_name_mapping = {
    "Paris": "Paris Saint-Germain",
    "Liverpool": "Liverpool",
    "Arsenal": "Arsenal",
    "Man City": "Manchester City",
    "Chelsea": "Chelsea",
    "Tottenham": "Tottenham",
    "Newcastle": "Newcastle",
    "Real Madrid": "Real Madrid",
    "Barcelona": "Barcelona",
    "Atleti": "Atlético Madrid",
    "Athletic Club": "Athletic Club",
    "Villarreal": "Villarreal",
    "Bayern München": "Bayern Munich",
    "Leverkusen": "Bayer Leverkusen",
    "B. Dortmund": "Borussia Dortmund",
    "Frankfurt": "Eintracht Frankfurt",
    "Inter": "Inter",
    "Atalanta": "Atalanta",
    "Juventus": "Juventus",
    "Napoli": "Napoli",
    "Marseille": "Marseille",
    "Monaco": "Monaco",
    "PSV": "PSV",
    "Ajax": "Ajax",
    "Benfica": "Benfica",
    "Sporting CP": "Sporting CP",
    "Club Brugge": "Club Brugge",
    "Union SG": "Union Saint-Gilloise",
    "Galatasaray": "Galatasaray",
    "Slavia Praha": "Slavia Praha",
    "Olympiacos": "Olympiacos",
    "Copenhagen": "Copenhagen",
    "Bodø/Glimt": "Bodø/Glimt",
    "Kairat Almaty": "Kairat Almaty",
    "Pafos": "Pafos",
    "Qarabağ": "Qarabağ"
}

# List of all teams in the competition
all_teams = [
    "Paris Saint-Germain", "Liverpool", "Arsenal", "Manchester City", "Chelsea",
    "Tottenham", "Newcastle", "Real Madrid", "Barcelona", "Atlético Madrid",
    "Athletic Club", "Villarreal", "Bayern Munich", "Bayer Leverkusen",
    "Borussia Dortmund", "Eintracht Frankfurt", "Inter", "Atalanta",
    "Juventus", "Napoli", "Marseille", "Monaco", "PSV", "Ajax",
    "Benfica", "Sporting CP", "Club Brugge", "Union Saint-Gilloise",
    "Galatasaray", "Slavia Praha", "Olympiacos", "Copenhagen",
    "Bodø/Glimt", "Kairat Almaty", "Pafos", "Qarabağ"
]


def get_day_of_week(date_str: str) -> str:
    """
    Takes a date string in the format 'MM/DD/YYYY HH:MM:SS'
    and returns the day of the week (e.g., 'Tuesday').
    """
    # Parse the date string into a datetime object
    dt = datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")

    # Return the full weekday name
    return dt.strftime("%A")


def get_uefa_fixtures_data():
    start_time = time.time()
    logging.info("Fetching fixtures data from UEFA.")
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/fixtures/fixtures_80_en.json")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    fixtures_by_matchday = {}
    
    # Process each matchday's fixtures
    for matchday_data in data["data"]["value"]:
        matchday_id = matchday_data.get("mdId", matchday_data.get("gdId", "unknown"))
        
        if "match" in matchday_data:
            fixtures_by_matchday[matchday_id] = []
            
            for match in matchday_data["match"]:
                # Get team names and map them to standardized names
                home_team = team_name_mapping.get(match["htName"], match["htName"])
                away_team = team_name_mapping.get(match["atName"], match["atName"])
                
                fixture_data = {
                    "matchday": matchday_id,
                    "match_id": match["mId"],
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_team_original": match["htName"],
                    "away_team_original": match["atName"],
                    "match_name": match.get("mdName", ""),
                    "date_time": match.get("dateTime", ""),
                    "match_status": match.get("matchStatus", "")
                }
                
                fixtures_by_matchday[matchday_id].append(fixture_data)
    
    end_time = time.time()
    logging.info(
        f"UEFA fixtures data fetched and processed in {end_time - start_time:.2f} seconds."
    )
    
    return fixtures_by_matchday


def create_opponents_table(fixtures_by_matchday):
    """
    Create a table showing each team's opponents across all matchdays.
    
    Args:
        fixtures_by_matchday: Dictionary containing fixtures organized by matchday
        
    Returns:
        Dictionary with team names as keys and their opponents by matchday as values
    """
    logging.info("Creating opponents table from fixtures data.")
    
    # Initialize opponents table
    opponents_table = {}
    for team in all_teams:
        opponents_table[team] = {}
    
    # Process each matchday
    for matchday_id, fixtures in fixtures_by_matchday.items():
        logging.info(f"Processing matchday {matchday_id} with {len(fixtures)} matches.")
        
        for fixture in fixtures:
            home_team = fixture["home_team"]
            away_team = fixture["away_team"]
            
            # Record opponents for both teams
            if home_team in opponents_table:
                opponents_table[home_team][f"Matchday {matchday_id}"] = away_team
            else:
                logging.warning(f"Home team {home_team} not found in team list")
                
            if away_team in opponents_table:
                opponents_table[away_team][f"Matchday {matchday_id}"] = home_team
            else:
                logging.warning(f"Away team {away_team} not found in team list")
    
    # Log summary
    total_matchdays = len(fixtures_by_matchday)
    logging.info(f"Opponents table created with {len(opponents_table)} teams across {total_matchdays} matchdays.")
    
    return opponents_table


def export_opponents_to_csv(opponents_table, filename="uefa_opponents_table.csv"):
    """
    Export the opponents table to a CSV file.
    
    Args:
        opponents_table: Dictionary containing team opponents by matchday
        filename: Name of the output CSV file
    """
    logging.info(f"Exporting opponents table to {filename}")
    
    if not opponents_table:
        logging.error("No opponents data to export")
        return
    
    # Get all unique matchdays and sort them
    all_matchdays = set()
    for team_data in opponents_table.values():
        all_matchdays.update(team_data.keys())
    
    # Sort matchdays numerically
    sorted_matchdays = sorted(all_matchdays, key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else 0)
    
    # Create CSV file
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        # Create fieldnames: Team, Matchday 1, Matchday 2, etc.
        fieldnames = ["Team"] + sorted_matchdays
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data for each team
        for team in sorted(all_teams):  # Sort teams alphabetically
            if team in opponents_table:
                row = {"Team": team}
                
                # Add opponent for each matchday
                for matchday in sorted_matchdays:
                    row[matchday] = opponents_table[team].get(matchday, "")
                
                writer.writerow(row)
            else:
                logging.warning(f"Team {team} not found in opponents table")
    
    logging.info(f"Successfully exported opponents table to {filename}")
    logging.info(f"CSV contains {len([team for team in all_teams if team in opponents_table])} teams and {len(sorted_matchdays)} matchdays")


def get_uefa_players_data():
    start_time = time.time()
    logging.info("Fetching players data from UEFA.")
    conn = http.client.HTTPSConnection("gaming.uefa.com")
    conn.request("GET", "/en/uclfantasy/services/feeds/players/players_80_en_2.json")
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))

    cleaned_player_data = []

    for player in data["data"]["value"]["playerList"]:
        # Transform the skill number to its description
        skill_description = skill_map.get(player.get("skill", 0), "unknown")

        cleaned_player_data.append(
            {
                "playerId": player.get("id", ""),
                "name": player.get("pDName", ""),
                "rating": player.get("rating", ""),
                "value": player.get("value", ""),
                "total points": player.get("totPts", ""),
                "goals": player.get("gS", ""),
                "assist": player.get("assist", ""),
                "minutes played": player.get("minsPlyd", ""),
                "average points": player.get("avgPlayerPts", ""),
                "isActive": player.get("isActive", ""),
                "team": player.get("cCode", ""),
                "man of match": player.get("mOM", ""),
                "position": skill_description,
                "goals conceded": player.get("gC"),
                "yellow cards": player.get("yC"),
                "red cards": player.get("rC"),
                "penalties earned": player.get("pE"),
                "balls recovered": player.get("bR"),
                "selected by (%)": player.get("selPer", ""),
                "match date": (
                    get_day_of_week(player["upcomingMatchesList"][0]["matchDate"])
                    if player.get("upcomingMatchesList")
                    else "N/A"
                ),
            }
        )

    end_time = time.time()
    logging.info(
        f"UEFA players data fetched and cleaned in {end_time - start_time:.2f} seconds."
    )

    return cleaned_player_data


def csv_table(player_data):
    # Write to a CSV file
    csv_file_path = "players_data.csv"

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "name",
            "rating",
            "value",
            "total points",
            "goals",
            "assist",
            "minutes played",
            "average points",
            "isActive",
            "team",
            "man of match",
            "position",
            "goals conceded",
            "yellow cards",
            "red cards",
            "penalties earned",
            "balls recovered",
            "selected by (%)",
            "match date",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for player in player_data:
            writer.writerow(player)

    print("CSV file created successfully.")


def main():
    """
    Main function to process UEFA fixtures and create opponents table.
    """
    try:
        # Fetch fixtures data from UEFA API
        logging.info("Starting UEFA fixtures processing...")
        fixtures_by_matchday = get_uefa_fixtures_data()
        
        if not fixtures_by_matchday:
            logging.error("No fixtures data retrieved. Exiting.")
            return
        
        # Create opponents table
        opponents_table = create_opponents_table(fixtures_by_matchday)
        
        # Export to CSV
        export_opponents_to_csv(opponents_table)
        
        # Display summary
        print("\n=== UEFA Champions League Opponents Table Created ===")
        print(f"Teams processed: {len([team for team in all_teams if team in opponents_table])}")
        print(f"Matchdays found: {len(fixtures_by_matchday)}")
        print("CSV file 'uefa_opponents_table.csv' created successfully!")
        
        # Display sample of the data
        print("\n=== Sample Data (first 3 teams) ===")
        sample_teams = sorted(all_teams)[:3]
        for team in sample_teams:
            if team in opponents_table:
                print(f"\n{team}:")
                for matchday, opponent in sorted(opponents_table[team].items()):
                    print(f"  {matchday}: vs {opponent}")
        
        return opponents_table
        
    except Exception as e:
        logging.error(f"Error processing UEFA fixtures: {str(e)}")
        raise


if __name__ == "__main__":
    # Run the complete opponents table generation
    main()
    
    # Uncomment below if you also want player data
    # uefa_players_data = get_uefa_players_data()
    # csv_table(uefa_players_data)
