#!/usr/bin/env python3
"""
Simple test script to validate the opponents algorithm for Paris Saint-Germain
using the sample fixture data
"""

import json
from src.core.team_mapper import TeamMapper

# Initialize team mapper
team_mapper = TeamMapper()
team_name_mapping = team_mapper.get_mapping_dict()

def test_paris_opponents():
    """Test finding Paris Saint-Germain's opponents from sample data"""
    print("=== Testing Paris Saint-Germain Opponents ===\n")
    
    # Load sample fixture data
    with open("tests/fixtures/fixture_sample.json", "r", encoding="utf-8") as f:
        sample_data = json.load(f)
    
    paris_opponents = {}
    
    print("Looking for Paris Saint-Germain matches in sample data...\n")
    
    # Process matches to find Paris (handle nested structure)
    for matchday_data in sample_data["data"]["value"]:
        if "match" not in matchday_data:
            continue
            
        for match in matchday_data["match"]:
            matchday_id = match.get("gdId", "1")  # Get gameday ID
            home_team_original = match["htName"]
            away_team_original = match["atName"]
            
            # Map to standardized names
            home_team = team_name_mapping.get(home_team_original, home_team_original)
            away_team = team_name_mapping.get(away_team_original, away_team_original)
            
            # Check if Paris is playing
            if home_team == "Paris Saint-Germain":
                opponent = away_team
                print(f"✅ Found Paris match - Matchday {matchday_id}: Paris Saint-Germain (Home) vs {opponent}")
                paris_opponents[f"Matchday {matchday_id}"] = opponent
                
            elif away_team == "Paris Saint-Germain":
                opponent = home_team
                print(f"✅ Found Paris match - Matchday {matchday_id}: {opponent} vs Paris Saint-Germain (Away)")
                paris_opponents[f"Matchday {matchday_id}"] = opponent
    
    # Display results
    if paris_opponents:
        print(f"\n=== Paris Saint-Germain Opponents Table ===")
        for matchday, opponent in sorted(paris_opponents.items()):
            print(f"{matchday}: vs {opponent}")
        
        # Create a simple CSV for Paris only
        with open("paris_opponents.csv", "w", encoding="utf-8") as f:
            f.write("Team,")
            f.write(",".join(sorted(paris_opponents.keys())))
            f.write("\n")
            f.write("Paris Saint-Germain,")
            f.write(",".join([paris_opponents[md] for md in sorted(paris_opponents.keys())]))
            f.write("\n")
        
        print(f"\nCSV file 'paris_opponents.csv' created!")
        
    else:
        print("❌ No matches found for Paris Saint-Germain in sample data")
        print("\nAvailable teams in sample data:")
        teams_found = set()
        for matchday_data in sample_data["data"]["value"]:
            if "match" not in matchday_data:
                continue
            for match in matchday_data["match"]:
                home_original = match["htName"]
                away_original = match["atName"]
                home_mapped = team_name_mapping.get(home_original, home_original)
                away_mapped = team_name_mapping.get(away_original, away_original)
                teams_found.add(f"{home_original} -> {home_mapped}")
                teams_found.add(f"{away_original} -> {away_mapped}")
        
        for team in sorted(teams_found):
            print(f"  - {team}")
    
    return paris_opponents

if __name__ == "__main__":
    test_paris_opponents()