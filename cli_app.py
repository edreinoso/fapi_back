"""
CLI Application for UEFA Champions League Fantasy Data Processor
"""
import argparse
import logging
import sys
from typing import Optional

from uefa_api_client import UEFAApiClient
from team_mapper import TeamMapper
from data_processors import FixturesDataProcessor, OpponentsTableBuilder, PlayersDataProcessor
from csv_exporter import CSVExporter


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
        self.players_processor = PlayersDataProcessor()
        self.csv_exporter = CSVExporter(self.team_mapper)
    
    def setup_logging(self):
        """Configure logging for the application"""
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
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
  python -m cli_app fixtures          # Process fixtures and create opponents table
  python -m cli_app players           # Process players data
  python -m cli_app fixtures --help   # Show fixtures-specific help
        """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Fixtures command
        fixtures_parser = subparsers.add_parser(
            'fixtures', 
            help='Process UEFA fixtures and create opponents table'
        )
        fixtures_parser.add_argument(
            '--output', '-o',
            default='uefa_opponents_table.csv',
            help='Output CSV filename (default: uefa_opponents_table.csv)'
        )
        
        # Players command
        players_parser = subparsers.add_parser(
            'players',
            help='Process UEFA players data'
        )
        players_parser.add_argument(
            '--output', '-o',
            default='players_data.csv',
            help='Output CSV filename (default: players_data.csv)'
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
            opponents_table = self.opponents_builder.build_opponents_table(fixtures_by_matchday)
            
            # Export to CSV
            success = self.csv_exporter.export_opponents_table(opponents_table, output_filename)
            
            if success:
                # Display summary
                print("\n=== UEFA Champions League Opponents Table Created ===")
                print(f"Teams processed: {len([team for team in self.team_mapper.get_all_teams() if team in opponents_table])}")
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
    
    def process_players_command(self, output_filename: str) -> bool:
        """
        Process players command
        
        Args:
            output_filename: Name of output CSV file
            
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
            
            # Process players
            players_data = self.players_processor.process_players(raw_data)
            if not players_data:
                self.logger.error("No players data to process")
                return False
            
            # Export to CSV
            success = self.csv_exporter.export_players_data(players_data, output_filename)
            
            if success:
                # Display summary
                print("\n=== UEFA Champions League Players Data Created ===")
                print(f"Players processed: {len(players_data)}")
                print(f"CSV file '{output_filename}' created successfully!")
                
                # Display sample of the data
                print("\n=== Sample Players (first 5) ===")
                for i, player in enumerate(players_data[:5], 1):
                    print(f"{i}. {player['name']} ({player['team']}) - {player['position']} - {player['rating']} rating")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error processing players: {str(e)}")
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
            if parsed_args.command == 'fixtures':
                print("🏆 Processing UEFA Champions League Fixtures...")
                success = self.process_fixtures_command(parsed_args.output)
                
                if success:
                    print(f"\n✅ Success! Check '{parsed_args.output}' for the opponents table.")
                    return 0
                else:
                    print("\n❌ Failed to process fixtures.")
                    return 1
                
            elif parsed_args.command == 'players':
                print("⚽ Processing UEFA Champions League Players...")
                success = self.process_players_command(parsed_args.output)
                
                if success:
                    print(f"\n✅ Success! Check '{parsed_args.output}' for the players data.")
                    return 0
                else:
                    print("\n❌ Failed to process players.")
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
