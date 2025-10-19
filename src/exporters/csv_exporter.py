"""
CSV export functionality for UEFA Champions League data
"""
import csv
import logging
from typing import Dict, List, Any

from src.core.team_mapper import TeamMapper


class CSVExporter:
    """Handles exporting data to CSV files"""
    
    def __init__(self, team_mapper: TeamMapper):
        self.team_mapper = team_mapper
        self.logger = logging.getLogger(__name__)
    
    def export_opponents_table(self, opponents_table: Dict[str, Dict[str, str]], filename: str = "uefa_opponents_table.csv") -> bool:
        """
        Export opponents table to CSV file
        
        Args:
            opponents_table: Dictionary containing team opponents by matchday
            filename: Name of the output CSV file
            
        Returns:
            True if export successful, False otherwise
        """
        self.logger.info(f"Exporting opponents table to {filename}")
        
        if not opponents_table:
            self.logger.error("No opponents data to export")
            return False
        
        try:
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
                for team in sorted(self.team_mapper.get_all_teams()):  # Sort teams alphabetically
                    if team in opponents_table:
                        row = {"Team": team}
                        
                        # Add opponent for each matchday
                        for matchday in sorted_matchdays:
                            row[matchday] = opponents_table[team].get(matchday, "")
                        
                        writer.writerow(row)
                    else:
                        self.logger.warning(f"Team {team} not found in opponents table")
            
            valid_teams = len([team for team in self.team_mapper.get_all_teams() if team in opponents_table])
            self.logger.info(f"Successfully exported opponents table to {filename}")
            self.logger.info(f"CSV contains {valid_teams} teams and {len(sorted_matchdays)} matchdays")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting opponents table: {str(e)}")
            return False
    
    def export_players_data(self, players_data: List[Dict[str, Any]], filename: str = "players_data.csv") -> bool:
        """
        Export players data to CSV file
        
        Args:
            players_data: List of player data dictionaries
            filename: Name of the output CSV file
            
        Returns:
            True if export successful, False otherwise
        """
        self.logger.info(f"Exporting players data to {filename}")
        
        if not players_data:
            self.logger.error("No players data to export")
            return False
        
        try:
            # Get all unique field names from players data
            all_fields = set()
            for player in players_data:
                all_fields.update(player.keys())
            
            # Define base fieldnames for players CSV
            base_fieldnames = [
                "playerId",
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
                "opponent",
                "home or away"
            ]
            
            # Find MD (matchday) columns and sort them
            md_fields = sorted([field for field in all_fields if field.startswith('MD') and field[2:].isdigit()], 
                              key=lambda x: int(x[2:]))
            
            # Combine base fields with MD fields
            fieldnames = base_fieldnames + md_fields
            
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for player in players_data:
                    writer.writerow(player)
            
            self.logger.info(f"Successfully exported {len(players_data)} players to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting players data: {str(e)}")
            return False