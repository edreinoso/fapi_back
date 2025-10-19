"""
Team analysis module for UEFA Champions League fantasy teams
"""
import http.client
import json
import logging
import urllib.parse
from typing import Dict, List, Any, Optional
from src.exporters.dynamodb_exporter import DynamoDBExporter


class TeamAnalyzer:
    """Analyzes fantasy team data by fetching from UEFA API and cross-referencing with DynamoDB"""
    
    BASE_HOST = "gaming.uefa.com"
    
    def __init__(self, dynamodb_exporter: Optional[DynamoDBExporter] = None):
        self.logger = logging.getLogger(__name__)
        self.dynamodb_exporter = dynamodb_exporter or DynamoDBExporter()
    
    def fetch_team_data(self, user_guid: str, matchday_id: int = 2, phase_id: int = 0) -> Optional[Dict[str, Any]]:
        """
        Fetch team data from UEFA API with authentication headers
        
        Args:
            user_guid: User GUID for the team
            matchday_id: Matchday ID (default: 2)
            phase_id: Phase ID (default: 0)
            
        Returns:
            Team data dictionary or None if failed
        """
        # Build the endpoint URL
        endpoint = f"/en/uclfantasy/services/api/Gameplay/user/{user_guid}/opponent-team"
        params = f"?matchdayId={matchday_id}&phaseId={phase_id}&opponentguid={user_guid}"
        full_path = endpoint + params
        
        # Headers based on your cURL command
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'access-control-expose-headers': 'Date',
            'dnt': '1',
            'entity': 'ed0t4n$3!',
            'priority': 'u=1, i',
            'referer': 'https://gaming.uefa.com/en/uclfantasy/team/18034ca6-8818-11f0-801e-7568b2125093/0041006200640065006c006c00610068/0/0/0/00330030003100360033003300300038',
            'sec-ch-ua': '"Not=A?Brand";v="24", "Chromium";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            # Note: Not including cookies as they contain sensitive session data
            # User will need to provide authentication if needed
        }
        
        try:
            self.logger.info(f"Fetching team data from {self.BASE_HOST}{full_path}")
            
            conn = http.client.HTTPSConnection(self.BASE_HOST)
            conn.request("GET", full_path, headers=headers)
            
            response = conn.getresponse()
            
            if response.status != 200:
                self.logger.error(f"HTTP {response.status}: {response.reason}")
                # If we get 401/403, suggest using the JSON file as fallback
                if response.status in [401, 403]:
                    self.logger.warning("Authentication required. Consider using the JSON file method as fallback.")
                return None
            
            data = response.read()
            parsed_data = json.loads(data.decode("utf-8"))
            
            self.logger.info("Successfully fetched team data from API")
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error fetching team data: {str(e)}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
    
    def load_team_from_json_fallback(self, json_file_path: str) -> Optional[Dict[str, Any]]:
        """
        Fallback method to load team data from JSON file if API fails
        
        Args:
            json_file_path: Path to the team JSON file
            
        Returns:
            Team data dictionary or None if failed
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                team_data = json.load(f)
            
            self.logger.info(f"Successfully loaded team data from {json_file_path}")
            return team_data
            
        except Exception as e:
            self.logger.error(f"Error loading team data from {json_file_path}: {str(e)}")
            return None
    
    def extract_player_ids(self, team_data: Dict[str, Any]) -> List[int]:
        """
        Extract player IDs from team data
        
        Args:
            team_data: Team data dictionary
            
        Returns:
            List of player IDs
        """
        try:
            players = team_data.get("data", {}).get("value", {}).get("playerid", [])
            player_ids = [player.get("id") for player in players if player.get("id")]
            
            self.logger.info(f"Extracted {len(player_ids)} player IDs from team data")
            return player_ids
            
        except Exception as e:
            self.logger.error(f"Error extracting player IDs: {str(e)}")
            return []
    
    def get_player_info_from_dynamodb(self, player_id: int, table_name: str = "new-manual-fapi-ddb") -> Optional[Dict[str, Any]]:
        """
        Get player information from DynamoDB
        
        Args:
            player_id: Player ID to lookup
            table_name: DynamoDB table name
            
        Returns:
            Player information dictionary or None if not found
        """
        try:
            player_info = self.dynamodb_exporter.get_player_by_id(str(player_id), table_name)
            if player_info:
                self.logger.debug(f"Found player info for ID {player_id}")
                return player_info
            else:
                self.logger.warning(f"No player info found for ID {player_id}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting player info for ID {player_id}: {str(e)}")
            return None
    
    def get_team_players_info(self, team_data: Dict[str, Any], table_name: str = "new-manual-fapi-ddb") -> List[Dict[str, Any]]:
        """
        Get complete player information for all team players
        
        Args:
            team_data: Team data dictionary
            table_name: DynamoDB table name
            
        Returns:
            List of player information dictionaries
        """
        player_ids = self.extract_player_ids(team_data)
        team_players = []
        
        # Get team players data for additional context
        team_players_data = team_data.get("data", {}).get("value", {}).get("playerid", [])
        team_players_dict = {player.get("id"): player for player in team_players_data}
        
        for player_id in player_ids:
            # Get player info from DynamoDB
            player_info = self.get_player_info_from_dynamodb(player_id, table_name)
            
            # Get team-specific player data
            team_player_data = team_players_dict.get(player_id, {})
            
            if player_info:
                # Combine DynamoDB info with team-specific data
                combined_info = {
                    "player_id": player_id,
                    "name": player_info.get("name", "Unknown"),
                    "position": player_info.get("position", "Unknown"),
                    "team": player_info.get("team", "Unknown"),
                    "rating": player_info.get("rating", "N/A"),
                    "value": team_player_data.get("value", "N/A"),
                    "overall_points": team_player_data.get("overallpoints", 0),
                    "is_captain": bool(team_player_data.get("iscaptain", 0)),
                    "bench_position": team_player_data.get("benchposition", 0),
                    "minutes_in_game": team_player_data.get("minutesingame"),
                    "is_active": bool(team_player_data.get("isactive", 0))
                }
                team_players.append(combined_info)
            else:
                # Fallback with minimal info if not found in DynamoDB
                combined_info = {
                    "player_id": player_id,
                    "name": f"Player {player_id} (Not found in DB)",
                    "position": "Unknown",
                    "team": "Unknown",
                    "rating": "N/A",
                    "value": team_player_data.get("value", "N/A"),
                    "overall_points": team_player_data.get("overallpoints", 0),
                    "is_captain": bool(team_player_data.get("iscaptain", 0)),
                    "bench_position": team_player_data.get("benchposition", 0),
                    "minutes_in_game": team_player_data.get("minutesingame"),
                    "is_active": bool(team_player_data.get("isactive", 0))
                }
                team_players.append(combined_info)
        
        return team_players
    
    def display_team_summary(self, team_data: Dict[str, Any], team_players: List[Dict[str, Any]]) -> None:
        """
        Display a formatted team summary
        
        Args:
            team_data: Team data dictionary
            team_players: List of player information dictionaries
        """
        # Extract team summary info
        team_info = team_data.get("data", {}).get("value", {})
        team_name = team_info.get("teamName", "Unknown Team")
        username = team_info.get("username", "Unknown User")
        team_value = team_info.get("teamValue", 0)
        team_balance = team_info.get("teamBalance", 0)
        overall_points = team_info.get("ovPoints", 0)
        overall_rank = team_info.get("ovRank", 0)
        gameday_points = team_info.get("gdPoints", 0)
        gameday_rank = team_info.get("gdRank", 0)
        
        print("\\n🏆 ═══════════════════════════════════════════════════════════")
        print(f"   {team_name} ({username})")
        print("═══════════════════════════════════════════════════════════")
        print(f"💰 Team Value: €{team_value}M | Balance: €{team_balance}M")
        print(f"📊 Overall Points: {overall_points} (Rank: {overall_rank:,})")
        print(f"📈 Gameday Points: {gameday_points} (Rank: {gameday_rank:,})")
        print()
        
        # Separate starting XI and bench
        starting_xi = [p for p in team_players if p["bench_position"] == 0]
        bench_players = [p for p in team_players if p["bench_position"] > 0]
        
        # Display starting XI
        print("🥅 STARTING XI:")
        print("─" * 80)
        
        for player in starting_xi:
            captain_indicator = " (C)" if player["is_captain"] else ""
            minutes_str = f"{player['minutes_in_game']}'" if player['minutes_in_game'] else "0'"
            
            print(f"  {player['name']:<25} {captain_indicator:<4} | "
                  f"{player['position']:<12} | {player['team']:<6} | "
                  f"€{player['value']:<4} | {player['overall_points']:<3} pts | {minutes_str}")
        
        # Display bench
        if bench_players:
            print("\\n🪑 BENCH:")
            print("─" * 80)
            
            for player in bench_players:
                minutes_str = f"{player['minutes_in_game']}'" if player['minutes_in_game'] else "0'"
                
                print(f"  {player['name']:<25}      | "
                      f"{player['position']:<12} | {player['team']:<6} | "
                      f"€{player['value']:<4} | {player['overall_points']:<3} pts | {minutes_str}")
        
        print("\\n═══════════════════════════════════════════════════════════")
    
    def analyze_team(self, user_guid: str, matchday_id: int = 2, phase_id: int = 0, 
                     table_name: str = "new-manual-fapi-ddb", json_fallback_path: Optional[str] = None) -> None:
        """
        Complete team analysis by fetching from API and cross-referencing with DynamoDB
        
        Args:
            user_guid: User GUID for the team
            matchday_id: Matchday ID (default: 2)
            phase_id: Phase ID (default: 0)
            table_name: DynamoDB table name
            json_fallback_path: Optional path to JSON file if API fails
        """
        # Try to fetch team data from API first
        team_data = self.fetch_team_data(user_guid, matchday_id, phase_id)
        
        # If API fails and we have a fallback JSON file, use it
        if not team_data and json_fallback_path:
            print("⚠️  API request failed, falling back to JSON file...")
            team_data = self.load_team_from_json_fallback(json_fallback_path)
        
        if not team_data:
            print("❌ Failed to load team data from both API and JSON file")
            return
        
        # Get player information
        print("🔍 Fetching player information from database...")
        team_players = self.get_team_players_info(team_data, table_name)
        
        if not team_players:
            print("❌ No players found")
            return
        
        # Display team summary
        self.display_team_summary(team_data, team_players)