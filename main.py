"""
UEFA Champions League Fantasy Data Processor - Legacy Entry Point

This file maintains backward compatibility with the old main.py interface
while using the new modular architecture.

Usage:
  python main.py fixtures        # Process fixtures and create opponents table
  python main.py players         # Process players data
  python main.py --help          # Show help
"""
from src.cli.app import main as cli_main


if __name__ == "__main__":
    cli_main()