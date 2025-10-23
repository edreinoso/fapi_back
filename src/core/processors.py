"""
Data processing classes for UEFA Champions League data
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.core.team_mapper import TeamMapper


class FixturesDataProcessor:
    """Processes raw fixtures data from UEFA API"""

    def __init__(self, team_mapper: TeamMapper):
        self.team_mapper = team_mapper
        self.logger = logging.getLogger(__name__)

    def process_fixtures(
        self, raw_data: Dict[str, Any]
    ) -> Dict[int, List[Dict[str, Any]]]:
        """
        Process raw fixtures data into organized structure

        Args:
            raw_data: Raw data from UEFA fixtures API

        Returns:
            Dictionary of fixtures organized by matchday
        """
        if not raw_data or "data" not in raw_data or "value" not in raw_data["data"]:
            self.logger.error("Invalid fixtures data structure")
            return {}

        fixtures_by_matchday = {}

        # Process each matchday's fixtures
        for matchday_data in raw_data["data"]["value"]:
            matchday_id = matchday_data.get(
                "mdId", matchday_data.get("gdId", "unknown")
            )

            if "match" not in matchday_data:
                continue

            fixtures_by_matchday[matchday_id] = []

            for match in matchday_data["match"]:
                # Get team names and map them to standardized names
                home_team = self.team_mapper.get_standardized_name(match["htName"])
                away_team = self.team_mapper.get_standardized_name(match["atName"])

                fixture_data = {
                    "matchday": matchday_id,
                    "match_id": match["mId"],
                    "home_team": home_team,
                    "away_team": away_team,
                    "home_team_original": match["htName"],
                    "away_team_original": match["atName"],
                    "match_name": match.get("mdName", ""),
                    "date_time": match.get("dateTime", ""),
                    "match_status": match.get("matchStatus", ""),
                }

                fixtures_by_matchday[matchday_id].append(fixture_data)

        self.logger.info(
            f"Processed fixtures for {len(fixtures_by_matchday)} matchdays"
        )
        return fixtures_by_matchday


class OpponentsTableBuilder:
    """Builds opponents table from processed fixtures data"""

    def __init__(self, team_mapper: TeamMapper):
        self.team_mapper = team_mapper
        self.logger = logging.getLogger(__name__)

    def build_opponents_table(
        self, fixtures_by_matchday: Dict[int, List[Dict[str, Any]]]
    ) -> Dict[str, Dict[str, str]]:
        """
        Build opponents table from fixtures data

        Args:
            fixtures_by_matchday: Processed fixtures data

        Returns:
            Dictionary with team names as keys and their opponents by matchday as values
        """
        self.logger.info("Building opponents table from fixtures data")

        # Initialize opponents table
        opponents_table = {}
        for team in self.team_mapper.get_all_teams():
            opponents_table[team] = {}

        # Process each matchday
        for matchday_id, fixtures in fixtures_by_matchday.items():
            self.logger.info(
                f"Processing matchday {matchday_id} with {len(fixtures)} matches"
            )

            for fixture in fixtures:
                home_team = fixture["home_team"]
                away_team = fixture["away_team"]

                # Record opponents for both teams
                if self.team_mapper.is_valid_team(home_team):
                    opponents_table[home_team][f"Matchday {matchday_id}"] = away_team
                else:
                    self.logger.warning(f"Home team {home_team} not found in team list")

                if self.team_mapper.is_valid_team(away_team):
                    opponents_table[away_team][f"Matchday {matchday_id}"] = home_team
                else:
                    self.logger.warning(f"Away team {away_team} not found in team list")

        # Log summary
        total_matchdays = len(fixtures_by_matchday)
        valid_teams = len([team for team in opponents_table if opponents_table[team]])
        self.logger.info(
            f"Opponents table created with {valid_teams} teams across {total_matchdays} matchdays"
        )

        return opponents_table


class PlayersDataProcessor:
    """Processes raw players data from UEFA API"""

    # Skill mapping
    SKILL_MAP = {1: "goal keepers", 2: "defenders", 3: "midfielders", 4: "attackers"}

    def __init__(self, api_client=None):
        self.logger = logging.getLogger(__name__)
        self.api_client = api_client

    def _get_day_of_week(self, date_str: str) -> str:
        """
        Get day of week from date string

        Args:
            date_str: Date string in format 'MM/DD/YYYY HH:MM:SS'

        Returns:
            Day of the week name
        """
        try:
            dt = datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
            return dt.strftime("%A")
        except (ValueError, TypeError):
            return "N/A"

    def process_players(
        self, raw_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Process raw players data into cleaned format

        Args:
            raw_data: Raw data from UEFA players API

        Returns:
            List of processed player data dictionaries
        """
        if not raw_data or "data" not in raw_data or "value" not in raw_data["data"]:
            self.logger.error("Invalid players data structure")
            return []

        if "playerList" not in raw_data["data"]["value"]:
            self.logger.error("No playerList found in data")
            return []

        cleaned_player_data = []

        for player in raw_data["data"]["value"]["playerList"]:
            # Transform the skill number to its description
            skill_description = self.SKILL_MAP.get(player.get("skill", 0), "unknown")

            for upcoming_match in player.get("upcomingMatchesList", []):
                home_or_away = upcoming_match.get("tLoc")
                opponent = upcoming_match.get("vsCCode")

            player_data = {
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
                    self._get_day_of_week(player["upcomingMatchesList"][0]["matchDate"])
                    if player.get("upcomingMatchesList")
                    else "N/A"
                ),
                "home or away": home_or_away,
                "opponent": opponent,
            }

            # Fetch fantasy points data if API client is available
            if self.api_client:
                fantasy_data = self._get_player_fantasy_points(player.get("id", ""))
                player_data.update(fantasy_data)

            cleaned_player_data.append(player_data)

        self.logger.info(f"Processed {len(cleaned_player_data)} players")
        return cleaned_player_data

    def _get_player_fantasy_points(self, player_id: str) -> Dict[str, int]:
        """
        Fetch and extract fantasy points for a single player

        Args:
            player_id: The player's ID

        Returns:
            Dictionary with matchday fantasy points (MD1, MD2, etc.)
        """
        fantasy_points = {}

        if not self.api_client or not player_id:
            return fantasy_points

        try:
            # Fetch player fantasy data from API
            raw_fantasy_data = self.api_client.fetch_player_fantasy_data(player_id)

            if not raw_fantasy_data or "data" not in raw_fantasy_data:
                # Player has no fantasy data (hasn't played), set default values
                self._set_default_fantasy_points(fantasy_points)
                return fantasy_points

            player_data = raw_fantasy_data["data"].get("value")
            if not player_data:
                # Player data is None (hasn't played), set default values
                self._set_default_fantasy_points(fantasy_points)
                return fantasy_points

            # Get points from matchdayPoints array first, then fallback to points array
            points_array = player_data.get(
                "matchdayPoints", player_data.get("points", [])
            )

            # Extract fantasy points for each matchday
            for i, points_data in enumerate(points_array):
                matchday_key = f"MD{i + 1}"
                fantasy_points[matchday_key] = points_data.get("tPoints", 0)

            # If no points data found, set default values
            if not fantasy_points:
                self._set_default_fantasy_points(fantasy_points)

        except Exception as e:
            # Log error but continue with default values
            self.logger.debug(
                f"Error fetching fantasy data for player {player_id}: {str(e)}"
            )
            self._set_default_fantasy_points(fantasy_points)

        return fantasy_points

    def _set_default_fantasy_points(self, fantasy_points: Dict[str, int]) -> None:
        """
        Set default fantasy points (0) for players who haven't played

        Args:
            fantasy_points: Dictionary to populate with default values
        """
        # Set up to 8 matchdays with 0 points (can be adjusted as needed)
        for i in range(1, 9):
            matchday_key = f"MD{i}"
            fantasy_points[matchday_key] = 0