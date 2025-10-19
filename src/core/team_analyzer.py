"""
Team analysis module for UEFA Champions League fantasy teams
"""

import csv
import http.client
import json
import logging
import urllib.parse
from typing import Any, Dict, List, Optional

from src.exporters.dynamodb_exporter import DynamoDBExporter
from src.exporters.csv_exporter import CSVExporter
from src.core.team_mapper import TeamMapper


class TeamAnalyzer:
    """Analyzes fantasy team data by fetching from UEFA API and cross-referencing with DynamoDB"""

    BASE_HOST = "gaming.uefa.com"

    def __init__(self, dynamodb_exporter: Optional[DynamoDBExporter] = None, csv_exporter: Optional[CSVExporter] = None):
        self.logger = logging.getLogger(__name__)
        self.dynamodb_exporter = dynamodb_exporter or DynamoDBExporter()
        self.csv_exporter = csv_exporter or CSVExporter(TeamMapper())

    def fetch_team_data(
        self, user_guid: str, matchday_id: int = 2, phase_id: int = 0
    ) -> Optional[Dict[str, Any]]:
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
        endpoint = (
            f"/en/uclfantasy/services/api/Gameplay/user/{user_guid}/opponent-team"
        )
        params = (
            f"?matchdayId={matchday_id}&phaseId={phase_id}&opponentguid={user_guid}"
        )
        full_path = endpoint + params

        # Headers based on your cURL command
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "access-control-expose-headers": "Date",
            "dnt": "1",
            "entity": "ed0t4n$3!",
            "priority": "u=1, i",
            "referer": "https://gaming.uefa.com/en/uclfantasy/team/18034ca6-8818-11f0-801e-7568b2125093/0041006200640065006c006c00610068/0/0/0/00330030003100360033003300300038",
            "sec-ch-ua": '"Not=A?Brand";v="24", "Chromium";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
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
                    self.logger.warning(
                        "Authentication required. Consider using the JSON file method as fallback."
                    )
                return None

            data = response.read()
            parsed_data = json.loads(data.decode("utf-8"))

            self.logger.info("Successfully fetched team data from API")
            return parsed_data

        except Exception as e:
            self.logger.error(f"Error fetching team data: {str(e)}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    def load_team_from_json_fallback(
        self, json_file_path: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fallback method to load team data from JSON file if API fails

        Args:
            json_file_path: Path to the team JSON file

        Returns:
            Team data dictionary or None if failed
        """
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                team_data = json.load(f)

            self.logger.info(f"Successfully loaded team data from {json_file_path}")
            return team_data

        except Exception as e:
            self.logger.error(
                f"Error loading team data from {json_file_path}: {str(e)}"
            )
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

    def get_player_info_from_dynamodb(
        self, player_id: int, table_name: str = "new-manual-fapi-ddb"
    ) -> Optional[Dict[str, Any]]:
        """
        Get player information from DynamoDB

        Args:
            player_id: Player ID to lookup
            table_name: DynamoDB table name

        Returns:
            Player information dictionary or None if not found
        """
        try:
            player_info = self.dynamodb_exporter.get_player_by_id(
                str(player_id), table_name
            )
            if player_info:
                self.logger.debug(f"Found player info for ID {player_id}")
                return player_info
            else:
                self.logger.warning(f"No player info found for ID {player_id}")
                return None

        except Exception as e:
            self.logger.error(f"Error getting player info for ID {player_id}: {str(e)}")
            return None

    def get_team_players_info(
        self, player_ids: List[int], table_name: str = "new-manual-fapi-ddb"
    ) -> List[Dict[str, Any]]:
        """
        Get complete player information for given player IDs from DynamoDB

        Args:
            player_ids: List of player IDs to lookup
            table_name: DynamoDB table name

        Returns:
            List of player information dictionaries
        """
        team_players = []

        for player_id in player_ids:
            # Get player info from DynamoDB
            player_info = self.get_player_info_from_dynamodb(player_id, table_name)

            if player_info:
                # Return all DynamoDB properties
                team_players.append(player_info)
            else:
                # Fallback with minimal info if not found in DynamoDB
                fallback_info = {
                    "playerId": str(player_id),
                    "name": f"Player {player_id} (Not found in DB)",
                    "position": "Unknown",
                    "team": "Unknown",
                    "rating": "N/A",
                }
                team_players.append(fallback_info)

        return team_players


    def analyze_team(
        self,
        user_guid: str,
        matchday_id: int = 2,
        phase_id: int = 0,
        table_name: str = "new-manual-fapi-ddb",
        json_fallback_path: Optional[str] = None,
        csv_filename: str = "my_team.csv",
    ) -> bool:
        """
        Complete team analysis by fetching from API, cross-referencing with DynamoDB, and exporting to CSV

        Args:
            user_guid: User GUID for the team
            matchday_id: Matchday ID (default: 2)
            phase_id: Phase ID (default: 0)
            table_name: DynamoDB table name
            json_fallback_path: Optional path to JSON file if API fails
            csv_filename: Output CSV filename

        Returns:
            True if successful, False otherwise
        """
        # Try to fetch team data from API first
        team_data = self.fetch_team_data(user_guid, matchday_id, phase_id)
        # print(team_data)
        # breakpoint()

        # If API fails and we have a fallback JSON file, use it
        if not team_data and json_fallback_path:
            print("⚠️  API request failed, falling back to JSON file...")
            team_data = self.load_team_from_json_fallback(json_fallback_path)

        if not team_data:
            print("❌ Failed to load team data from both API and JSON file")
            return False

        # Get player information
        print("🔍 Fetching player information from database...")
        player_ids = self.extract_player_ids(team_data)
        team_players = self.get_team_players_info(player_ids, table_name)

        if not team_players:
            print("❌ No players found")
            return False

        # Export team to CSV using CSVExporter
        success = self.csv_exporter.export_players_data(team_players, csv_filename)

        if success:
            team_info = team_data.get("data", {}).get("value", {})
            team_name = team_info.get("teamName", "Unknown Team")
            print(f"✅ Successfully exported team '{team_name}' to '{csv_filename}'")
            print(f"📊 {len(team_players)} players exported")
        else:
            print("❌ Failed to export team to CSV")

        return success
