"""
Team name mapping and standardization
"""
from typing import List, Dict


class TeamMapper:
    """Handles mapping between API team names and standardized team names"""
    
    # Team name mapping - API names to standardized names
    TEAM_NAME_MAPPING = {
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
    ALL_TEAMS = [
        "Paris Saint-Germain", "Liverpool", "Arsenal", "Manchester City", "Chelsea",
        "Tottenham", "Newcastle", "Real Madrid", "Barcelona", "Atlético Madrid",
        "Athletic Club", "Villarreal", "Bayern Munich", "Bayer Leverkusen",
        "Borussia Dortmund", "Eintracht Frankfurt", "Inter", "Atalanta",
        "Juventus", "Napoli", "Marseille", "Monaco", "PSV", "Ajax",
        "Benfica", "Sporting CP", "Club Brugge", "Union Saint-Gilloise",
        "Galatasaray", "Slavia Praha", "Olympiacos", "Copenhagen",
        "Bodø/Glimt", "Kairat Almaty", "Pafos", "Qarabağ"
    ]
    
    def __init__(self):
        pass
    
    def get_standardized_name(self, api_name: str) -> str:
        """
        Get standardized team name from API name
        
        Args:
            api_name: Team name as returned by the API
            
        Returns:
            Standardized team name
        """
        return self.TEAM_NAME_MAPPING.get(api_name, api_name)
    
    def get_all_teams(self) -> List[str]:
        """
        Get list of all teams in the competition
        
        Returns:
            List of all standardized team names
        """
        return self.ALL_TEAMS.copy()
    
    def is_valid_team(self, team_name: str) -> bool:
        """
        Check if a team name is valid (exists in the competition)
        
        Args:
            team_name: Team name to check
            
        Returns:
            True if team exists in the competition
        """
        return team_name in self.ALL_TEAMS
    
    def get_mapping_dict(self) -> Dict[str, str]:
        """
        Get the complete team name mapping dictionary
        
        Returns:
            Dictionary mapping API names to standardized names
        """
        return self.TEAM_NAME_MAPPING.copy()