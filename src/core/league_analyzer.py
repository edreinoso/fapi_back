"""
League analysis module for UEFA Champions League fantasy leagues
"""

import http.client
import json
import logging
from collections import Counter
from typing import Any, Dict, List, Optional


class LeagueAnalyzer:
    """Analyzes fantasy league data by fetching from UEFA API and calculating player ownership"""

    BASE_HOST = "gaming.uefa.com"

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_league_data(
        self,
        league_id: int,
        opt_type: int = 1,
        phase_id: int = 0,
        matchday_id: int = 0,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch league leaderboard data from UEFA API

        Args:
            league_id: League ID
            opt_type: Option type (default: 1)
            phase_id: Phase ID (default: 0)
            matchday_id: Matchday ID (default: 0)

        Returns:
            League data dictionary or None if failed
        """

        endpoint = f"/en/uclfantasy/services/api/Leagues/{league_id}/leagueleaderboard"
        params = (
            f"?optType={opt_type}&phaseId={phase_id}&matchdayId={matchday_id}"
            f"&vPageChunk=25&vPageNo=1&vPageOneChunk=25&leagueID={league_id}"
            f"&buster=7v75kwgzi1758376863300"
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
            "sec-ch-ua": '"Not=A?Brand";v="24", "Chromium";v="140"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
        }

        try:
            self.logger.info(f"Fetching league data from {self.BASE_HOST}{full_path}")

            conn = http.client.HTTPSConnection(self.BASE_HOST)
            conn.request("GET", full_path, headers=headers)

            response = conn.getresponse()

            if response.status != 200:
                self.logger.error(f"HTTP {response.status}: {response.reason}")
                if response.status in [401, 403]:
                    self.logger.warning(
                        "Authentication required. Consider using the JSON file method as fallback."
                    )
                return None

            data = response.read()
            parsed_data = json.loads(data.decode("utf-8"))

            # Check if the response is successful
            if not parsed_data.get("meta", {}).get("success", False):
                message = parsed_data.get("meta", {}).get("message", "Unknown error")
                self.logger.warning(f"API request unsuccessful: {message}")
                return None

            self.logger.info("Successfully fetched league data from API")
            return parsed_data

        except Exception as e:
            self.logger.error(f"Error fetching league data: {str(e)}")
            return None
        finally:
            if "conn" in locals():
                conn.close()

    def load_league_from_json_fallback(
        self, json_file_path: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fallback method to load league data from JSON file if API fails

        Args:
            json_file_path: Path to the league JSON file

        Returns:
            League data dictionary or None if failed
        """
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                league_data = json.load(f)

            self.logger.info(f"Successfully loaded league data from {json_file_path}")
            return league_data

        except Exception as e:
            self.logger.error(
                f"Error loading league data from {json_file_path}: {str(e)}"
            )
            return None

    def calculate_player_ownership(
        self, league_data: Dict[str, Any], my_team_player_ids: List[int]
    ) -> Dict[int, float]:
        """
        Calculate what percentage of OTHER league competitors own each of YOUR players

        Args:
            league_data: League data dictionary from API or JSON
            my_team_player_ids: List of player IDs from your team

        Returns:
            Dictionary mapping your player_id to percentage of competitors who also own that player
        """
        try:
            # Extract league members from data.value.rest
            data_section = league_data.get("data", {})
            value_section = data_section.get("value", {}) if isinstance(data_section, dict) else {}
            league_members = value_section.get("rest", []) if isinstance(value_section, dict) else []

            if not league_members:
                self.logger.error("No league members found in data")
                return {}

            total_members = len(league_members)
            self.logger.info(f"Analyzing {total_members} league members")
            self.logger.info(f"Your team has {len(my_team_player_ids)} players")

            # For each of YOUR players, count how many competitors also own them
            ownership_counts = {player_id: 0 for player_id in my_team_player_ids}

            for member in league_members:
                # Ensure member is a dict
                if not isinstance(member, dict):
                    self.logger.warning(f"Unexpected member type: {type(member)}")
                    continue
                    
                user_players = member.get("userPlayers", [])
                if user_players and isinstance(user_players, list):
                    # Convert to set for faster lookup
                    competitor_player_ids = set(user_players)
                    
                    # Check which of YOUR players this competitor also owns
                    for my_player_id in my_team_player_ids:
                        if my_player_id in competitor_player_ids:
                            ownership_counts[my_player_id] += 1

            # Calculate ownership percentages
            ownership_percentages = {}
            for player_id, count in ownership_counts.items():
                ownership_percentages[player_id] = (count / total_members) * 100

            self.logger.info(
                f"Calculated ownership for {len(ownership_percentages)} of your players"
            )
            return ownership_percentages

        except Exception as e:
            self.logger.error(f"Error calculating player ownership: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            return {}
