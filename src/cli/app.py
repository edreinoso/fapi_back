"""
CLI Application for UEFA Champions League Fantasy Data Processor
"""

import argparse
import logging
import sys
from typing import Optional

from src.api.client import UEFAApiClient
from src.core.processors import (
    FixturesDataProcessor,
    OpponentsTableBuilder,
    PlayersDataProcessor,
)
from src.core.team_mapper import TeamMapper
from src.core.team_analyzer import TeamAnalyzer
from src.core.league_analyzer import LeagueAnalyzer
from src.exporters.csv_exporter import CSVExporter
from src.exporters.dynamodb_exporter import DynamoDBExporter


class CLIApp:
    """Main CLI application class"""

    def __init__(self):
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

        # Initialize components
        self.api_client = UEFAApiClient()
        self.team_mapper = TeamMapper()
        self.fixtures_processor = FixturesDataProcessor(self.team_mapper)
        self.opponents_builder = OpponentsTableBuilder(self.team_mapper)
        self.players_processor = PlayersDataProcessor(self.api_client)
        self.csv_exporter = CSVExporter(self.team_mapper)
        self.dynamodb_exporter = DynamoDBExporter()
        self.team_analyzer = TeamAnalyzer(self.dynamodb_exporter)
        self.league_analyzer = LeagueAnalyzer()

    def setup_logging(self):
        """Configure logging for the application"""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create and configure argument parser

        Returns:
            Configured ArgumentParser instance
        """
        parser = argparse.ArgumentParser(
            description="UEFA Champions League Fantasy Data Processor",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""Examples:
  uv run src/main.py fixtures                    # Process fixtures and create opponents table
  uv run src/main.py players                     # Process players data to CSV (default)
  uv run src/main.py players csv                 # Process players data to CSV
  uv run src/main.py players ddb                 # Process players data to DynamoDB
  uv run src/main.py players ddb -o my-table     # Export to custom DynamoDB table
  uv run src/main.py players ddb --region eu-west-1  # Use different AWS region
  uv run src/main.py team 3f10f14a-80b6-11f0-b138-750c902f7cf8  # Export your fantasy team to CSV
  uv run src/main.py team <guid> -o my_team_analysis.csv  # Export with custom filename
  uv run src/main.py team <guid> -m 3 -j json/team.json  # Use matchday 3 with JSON fallback
  uv run src/main.py team <guid> -m 3 -e my-fantasy-team  # Export team to DynamoDB table
  uv run src/main.py league 30163308 -t my-fantasy-team  # Analyze league ownership for your team
  uv run src/main.py league 30163308 -t my-fantasy-team -j json/players_in_league.json  # With JSON fallback
        """
        )

        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # Fixtures command
        fixtures_parser = subparsers.add_parser(
            "fixtures", help="Process UEFA fixtures and create opponents table"
        )
        fixtures_parser.add_argument(
            "--output",
            "-o",
            default="uefa_opponents_table.csv",
            help="Output CSV filename (default: uefa_opponents_table.csv)",
        )

        # Players command
        players_parser = subparsers.add_parser(
            "players", help="Process UEFA players data"
        )
        players_parser.add_argument(
            "format",
            choices=["csv", "ddb"],
            nargs="?",
            default="csv",
            help="Output format: csv for CSV file, ddb for DynamoDB (default: csv)",
        )
        players_parser.add_argument(
            "--output",
            "-o",
            help="Output filename for CSV (default: players_data.csv) or table name for DynamoDB (default: uefa-players)",
        )
        players_parser.add_argument(
            "--region",
            default="eu-central-1",
            help="AWS region for DynamoDB (default: eu-central-1)",
        )

        # Team command
        team_parser = subparsers.add_parser(
            "team", help="Analyze your UEFA fantasy team"
        )
        team_parser.add_argument(
            "user_guid",
            help="Your UEFA fantasy user GUID (e.g., 3f10f14a-80b6-11f0-b138-750c902f7cf8)",
        )
        team_parser.add_argument(
            "--matchday",
            "-m",
            type=int,
            help="Matchday ID",
        )
        team_parser.add_argument(
            "--phase",
            "-p",
            type=int,
            default=0,
            help="Phase ID (default: 0)",
        )
        team_parser.add_argument(
            "--table-name",
            "-t",
            default="new-manual-fapi-ddb",
            help="DynamoDB table name for fetching player data (default: new-manual-fapi-ddb)",
        )
        team_parser.add_argument(
            "--export-table",
            "-e",
            help="DynamoDB table name to export your team to (e.g., my-fantasy-team)",
        )
        team_parser.add_argument(
            "--json-fallback",
            "-j",
            help="Path to JSON file as fallback if API fails",
        )
        team_parser.add_argument(
            "--output",
            "-o",
            default="my_team.csv",
            help="Output CSV filename (default: my_team.csv)",
        )

        # League command
        league_parser = subparsers.add_parser(
            "league", help="Analyze league player ownership for your team"
        )
        league_parser.add_argument(
            "league_id",
            type=int,
            help="League ID (e.g., 30163308)",
        )
        league_parser.add_argument(
            "--team-table",
            "-t",
            required=True,
            help="DynamoDB table name where your team is stored (e.g., my-fantasy-team)",
        )
        league_parser.add_argument(
            "--json-fallback",
            "-j",
            help="Path to JSON file as fallback if API fails (e.g., json/players_in_league.json)",
        )
        league_parser.add_argument(
            "--output",
            "-o",
            default="my_team_with_ownership.csv",
            help="Output CSV filename (default: my_team_with_ownership.csv)",
        )

        return parser

    def process_fixtures_command(self, output_filename: str) -> bool:
        """
        Process fixtures command

        Args:
            output_filename: Name of output CSV file

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Starting UEFA fixtures processing")

            # Fetch raw data
            raw_data = self.api_client.fetch_fixtures_data()
            if not raw_data:
                self.logger.error("Failed to fetch fixtures data")
                return False

            # Process fixtures
            fixtures_by_matchday = self.fixtures_processor.process_fixtures(raw_data)
            if not fixtures_by_matchday:
                self.logger.error("No fixtures data to process")
                return False

            # Build opponents table
            opponents_table = self.opponents_builder.build_opponents_table(
                fixtures_by_matchday
            )

            # Export to CSV
            success = self.csv_exporter.export_opponents_table(
                opponents_table, output_filename
            )

            if success:
                # Display summary
                print("\n=== UEFA Champions League Opponents Table Created ===")
                print(
                    f"Teams processed: {len([team for team in self.team_mapper.get_all_teams() if team in opponents_table])}"
                )
                print(f"Matchdays found: {len(fixtures_by_matchday)}")
                print(f"CSV file '{output_filename}' created successfully!")

                # Display sample of the data
                print("\n=== Sample Data (first 3 teams) ===")
                sample_teams = sorted(self.team_mapper.get_all_teams())[:3]
                for team in sample_teams:
                    if team in opponents_table:
                        print(f"\n{team}:")
                        for matchday, opponent in sorted(opponents_table[team].items()):
                            print(f"  {matchday}: vs {opponent}")

            return success

        except Exception as e:
            self.logger.error(f"Error processing fixtures: {str(e)}")
            return False

    def process_players_command(
        self,
        format_type: str,
        output_target: Optional[str] = None,
        region: str = "eu-central-1",
    ) -> bool:
        """
        Process players command with support for multiple output formats

        Args:
            format_type: Output format ('csv' or 'ddb')
            output_target: Output filename for CSV or table name for DynamoDB
            region: AWS region for DynamoDB

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Starting UEFA players processing")

            # Fetch raw data
            raw_data = self.api_client.fetch_players_data()
            if not raw_data:
                self.logger.error("Failed to fetch players data")
                return False

            # Process players with fantasy points
            # This is the entry point of the application
            players_data = self.players_processor.process_players(raw_data)
            if not players_data:
                self.logger.error("No players data to process")
                return False

            # Export based on format type
            if format_type == "csv":
                output_filename = output_target or "players_data.csv"
                success = self.csv_exporter.export_players_data(
                    players_data, output_filename
                )

                if success:
                    print("\n=== UEFA Champions League Players Data Created ===")
                    print(f"Players processed: {len(players_data)}")
                    print(f"CSV file '{output_filename}' created successfully!")

            elif format_type == "ddb":
                table_name = output_target or "new-manual-fapi-ddb"
                # Update DynamoDB exporter region if needed
                if region != "eu-central-1":
                    self.dynamodb_exporter.region_name = region
                    self.dynamodb_exporter._dynamodb = (
                        None  # Reset client for new region
                    )

                success = self.dynamodb_exporter.export_players_data(
                    players_data, table_name
                )

                if success:
                    print(
                        "\n=== UEFA Champions League Players Data Exported to DynamoDB ==="
                    )
                    print(f"Players processed: {len(players_data)}")
                    print(f"DynamoDB table '{table_name}' updated successfully!")
                    print(f"Region: {region}")

            # Display sample of the data for both formats
            if success:
                print("\n=== Sample Players (first 5) ===")
                for i, player in enumerate(players_data[:5], 1):
                    print(
                        f"{i}. {player['name']} ({player['team']}) - {player['position']} - {player['rating']} rating"
                    )

            return success

        except Exception as e:
            self.logger.error(f"Error processing players: {str(e)}")
            return False

    def process_league_command(
        self,
        league_id: int,
        team_table_name: str,
        json_fallback_path: Optional[str] = None,
        output_filename: str = "my_team_with_ownership.csv",
    ) -> bool:
        """
        Process league command: analyze ownership and export team with ownership data

        Args:
            league_id: League ID to analyze
            team_table_name: DynamoDB table containing your team
            json_fallback_path: Optional path to JSON file if API fails
            output_filename: Output CSV filename

        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Starting league analysis for league {league_id}")

            # Step 1: Fetch league data
            print(f"🔍 Fetching league data for league ID {league_id}...")
            league_data = self.league_analyzer.fetch_league_data(league_id)

            # Fallback to JSON if API fails
            if not league_data and json_fallback_path:
                print("⚠️  API request failed, falling back to JSON file...")
                league_data = self.league_analyzer.load_league_from_json_fallback(
                    json_fallback_path
                )

            if not league_data:
                self.logger.error("Failed to fetch league data")
                return False

            # Step 2: Scan team from DynamoDB first
            print(f"\n🔍 Loading your team from DynamoDB table '{team_table_name}'...")
            team_players = self.dynamodb_exporter.list_all_players(team_table_name)

            if not team_players:
                self.logger.error(f"No players found in table '{team_table_name}'")
                print(f"❌ No team data found in table '{team_table_name}'")
                print("   Make sure you've exported your team first using:")
                print(f"   uv run main.py team <guid> -m 3 -e {team_table_name}")
                return False

            print(f"✅ Loaded {len(team_players)} players from your team")

            # Step 3: Extract player IDs from your team
            my_team_player_ids = [int(player.get("playerId", 0)) for player in team_players if player.get("playerId")]
            print(f"📋 Extracted {len(my_team_player_ids)} player IDs from your team")

            # Step 4: Calculate player ownership for YOUR players
            print("\n📊 Calculating how many competitors own YOUR players...")
            ownership_data = self.league_analyzer.calculate_player_ownership(league_data, my_team_player_ids)

            if not ownership_data:
                self.logger.error("Failed to calculate player ownership")
                return False

            league_name = (
                league_data.get("data", {}).get("value", {}).get("leagueName", "Unknown League")
            )
            total_members = len(league_data.get("data", {}).get("value", {}).get("rest", []))
            print(f"✅ Analyzed league '{league_name}' with {total_members} members")
            print(f"📈 Calculated ownership for {len(ownership_data)} of your players")

            # Step 5: Export to CSV with ownership data
            print(f"\n📝 Exporting team with ownership data to '{output_filename}'...")
            success = self.csv_exporter.export_players_data(
                team_players, output_filename, ownership_data
            )

            if success:
                print(f"\n✅ Successfully created '{output_filename}' with league ownership data!")
                print(f"📊 {len(team_players)} players with ownership percentages")
                
                # Show ownership summary
                print("\n=== Ownership Summary ===")
                for player in team_players[:5]:  # Show first 5 players
                    player_id = int(player.get("playerId", 0))
                    ownership = ownership_data.get(player_id, 0.0)
                    player_name = player.get("name", "Unknown")
                    print(f"{player_name}: {ownership:.1f}% owned in league")
                
                if len(team_players) > 5:
                    print(f"... and {len(team_players) - 5} more players")
            else:
                print("❌ Failed to export CSV")

            return success

        except Exception as e:
            self.logger.error(f"Error processing league: {str(e)}")
            return False

    def run(self, args: Optional[list] = None) -> int:
        """
        Run the CLI application

        Args:
            args: Command line arguments (for testing)

        Returns:
            Exit code (0 for success, 1 for error)
        """
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)

        if not parsed_args.command:
            parser.print_help()
            return 1

        try:
            if parsed_args.command == "fixtures":
                print("🏆 Processing UEFA Champions League Fixtures...")
                success = self.process_fixtures_command(parsed_args.output)

                if success:
                    print(
                        f"\n✅ Success! Check '{parsed_args.output}' for the opponents table."
                    )
                    return 0
                else:
                    print("\n❌ Failed to process fixtures.")
                    return 1

            elif parsed_args.command == "players":
                format_type = getattr(parsed_args, "format", "csv")
                if format_type == "ddb":
                    print("⚽ Processing UEFA Champions League Players for DynamoDB...")
                else:
                    print("⚽ Processing UEFA Champions League Players for CSV export...")

                success = self.process_players_command(
                    format_type=format_type,
                    output_target=parsed_args.output,
                    region=getattr(parsed_args, "region", "eu-central-1"),
                )

                if success:
                    if format_type == "ddb":
                        table_name = parsed_args.output or "uefa-players"
                        print(
                            f"\n✅ Success! Players data exported to DynamoDB table '{table_name}'."
                        )
                    else:
                        output_file = parsed_args.output or "players_data.csv"
                        print(
                            f"\n✅ Success! Check '{output_file}' for the players data."
                        )
                    return 0
                else:
                    print("\n❌ Failed to process players.")
                    return 1

            elif parsed_args.command == "team":
                print("🏆 Analyzing UEFA Champions League Fantasy Team...")
                
                try:
                    success = self.team_analyzer.analyze_team(
                        user_guid=parsed_args.user_guid,
                        matchday_id=parsed_args.matchday or 3,
                        phase_id=parsed_args.phase,
                        table_name=parsed_args.table_name,
                        json_fallback_path=parsed_args.json_fallback,
                        csv_filename=parsed_args.output,
                        export_to_dynamodb=bool(parsed_args.export_table),
                        dynamodb_table_name=parsed_args.export_table,
                    )
                    return 0 if success else 1
                except Exception as e:
                    print(f"\n❌ Error analyzing team: {str(e)}")
                    return 1

            elif parsed_args.command == "league":
                print("🏆 Analyzing League Ownership for Your Fantasy Team...")
                
                try:
                    success = self.process_league_command(
                        league_id=parsed_args.league_id,
                        team_table_name=parsed_args.team_table,
                        json_fallback_path=parsed_args.json_fallback,
                        output_filename=parsed_args.output,
                    )
                    
                    if success:
                        print(f"\n✅ Success! Check '{parsed_args.output}' for your team with ownership data.")
                        return 0
                    else:
                        print("\n❌ Failed to analyze league ownership.")
                        return 1
                except Exception as e:
                    print(f"\n❌ Error analyzing league: {str(e)}")
                    return 1

            else:
                print(f"Unknown command: {parsed_args.command}")
                parser.print_help()
                return 1

        except KeyboardInterrupt:
            print("\n⏹️  Process interrupted by user")
            return 0
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            return 1


def main():
    """Entry point for the CLI application"""
    app = CLIApp()
    exit_code = app.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
