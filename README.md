# ⚽ UEFA Champions League Fantasy Data Processor

A comprehensive command-line application to fetch, process, and analyze UEFA Champions League fantasy football data. Features include player statistics with matchday fantasy points, team fixtures with opponent tables, personal team analysis, and flexible export options to CSV and DynamoDB.

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📝 Installation](#-installation)
- [💻 Usage](#-usage)
- [📊 Output Files](#-output-files)
- [🏆 Teams Supported](#-teams-supported)
- [🏗️ Architecture](#️-architecture)
- [🚀 Development](#-development)
- [🔧 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

## ✨ Features

### 🏆 Core Functionality
- **🏆 Fixtures Processing**: Creates comprehensive opponents tables showing who each team plays in each matchday
- **⚽ Players Processing**: Fetches detailed player statistics with fantasy points breakdown by matchday (MD1, MD2, etc.)
- **🎯 Personal Team Analysis**: Analyze your UEFA fantasy team with player details from your lineup

### 📊 Export Options
- **📊 CSV Export**: Export data to clean, well-formatted CSV files for analysis
- **💾 DynamoDB Export**: Store player data in AWS DynamoDB for scalable cloud storage
- **📁 Team Export**: Export your personal fantasy team lineup to CSV or DynamoDB

### 🚀 Advanced Features
- **🎯 Fantasy Points**: Individual matchday fantasy points (MD1, MD2, etc.) for each player
- **🏅 Team Name Mapping**: Intelligent handling of team name variations between API sources
- **🏗️ Modular Architecture**: Professional code organization with separation of concerns
- **💻 CLI Interface**: User-friendly command-line interface with helpful error messages
- **📝 Comprehensive Logging**: Detailed logging for debugging and monitoring
- **🔄 Clean Execution**: No .pyc file generation with wrapper script

## 💻 Usage

### 🎯 Quick Start Commands

```bash
# Show main help
./run.sh --help                    # Using clean wrapper script
uv run main.py --help              # Direct execution

# Process fixtures and create opponents table
./run.sh fixtures
# → Creates: uefa_opponents_table.csv

# Process players with fantasy points (MD1, MD2, etc.)
./run.sh players csv
# → Creates: players_data.csv (includes fantasy points)

# Export players to DynamoDB
./run.sh players ddb
# → Creates/updates: new-manual-fapi-ddb table in DynamoDB

# Analyze your fantasy team and export to CSV
./run.sh team 3f10f14a-80b6-11f0-b138-750c902f7cf8
# → Creates: my_team.csv with your team lineup

# Export your fantasy team to DynamoDB
./run.sh team 3f10f14a-80b6-11f0-b138-750c902f7cf8 -m 3 -e my-fantasy-team
# → Exports to DynamoDB table 'my-fantasy-team' (skips CSV)
```

### 🚀 Advanced Usage

```bash
# 🏆 FIXTURES PROCESSING
# Custom output filenames
./run.sh fixtures --output my_opponents_2024.csv
./run.sh fixtures -o champions_league_fixtures.csv

# ⚽ PLAYERS PROCESSING WITH FANTASY POINTS
# Export to CSV with fantasy points (MD1, MD2, etc.)
./run.sh players csv --output uefa_players_with_points.csv
./run.sh players csv -o detailed_player_stats.csv

# Export to DynamoDB with custom settings
./run.sh players ddb --output my-uefa-table --region eu-west-1
./run.sh players ddb -o champions-data -t custom-table

# 🎯 TEAM ANALYSIS
# Analyze your team with custom output (CSV)
./run.sh team <your-guid> --output my_team_analysis.csv
./run.sh team <your-guid> -o team_matchday3.csv --matchday 3

# Export team to DynamoDB instead of CSV
./run.sh team <your-guid> -m 3 --export-table my-fantasy-team
./run.sh team <your-guid> --matchday 3 -e team-backup-table

# Use different table for fetching player data
./run.sh team <your-guid> --table-name my-players-table -e my-fantasy-team

# Fallback to JSON file if API fails
./run.sh team <your-guid> --json-fallback json/my_team_backup.json

# 📝 Get detailed help for specific commands
./run.sh fixtures --help
./run.sh players --help
./run.sh team --help
```

### Command Examples with Expected Output

```bash
# Example: Process fixtures
$ python main.py fixtures
🏆 Processing UEFA Champions League Fixtures...

=== UEFA Champions League Opponents Table Created ===
Teams processed: 36
Matchdays found: 8
CSV file 'uefa_opponents_table.csv' created successfully!

=== Sample Data (first 3 teams) ===

Ajax:
  Matchday 8: vs Inter
  Matchday 12: vs Real Madrid
  ...

✅ Success! Check 'uefa_opponents_table.csv' for the opponents table.
```

## 📊 Output Files

### 🏆 Fixtures Command
- **Default**: `uefa_opponents_table.csv`
- **Format**: Teams as rows, matchdays as columns, opponents as cell values
- **Content**: Who each team plays in each matchday of the Champions League

### ⚽ Players Command
- **Default**: `players_data.csv`
- **New Feature**: Includes **fantasy points by matchday** (MD1, MD2, MD3, etc.)
- **Content**: Comprehensive player statistics including:
  - Basic info: Name, rating, value, total points
  - Performance: Goals, assists, minutes played
  - Fantasy data: **MD1, MD2, MD3, etc. fantasy points**
  - Details: Position, team, selection percentage
  - And much more...

### 🎯 Team Command
- **Default**: `my_team.csv` (or DynamoDB table if using `-e` flag)
- **Export Options**:
  - CSV: Use default or specify with `-o` flag
  - DynamoDB: Use `-e` flag with table name (skips CSV export)
- **Content**: Your personal fantasy team lineup including:
  - Player ID, name, rating, value
  - Captain status, bench position
  - Minutes played, active status
  - Starting eleven indicator

### 💾 DynamoDB Export
- **Default table**: `new-manual-fapi-ddb` (for player data)
- **Team export**: Use `-e <table-name>` flag to export your fantasy team
- **Content**: All player data or team lineup stored in AWS DynamoDB
- **Benefits**: Scalable cloud storage, queryable data, team collaboration

## 📊 Example Output

### 🏆 Opponents Table (fixtures)
```csv
Team,Matchday 1,Matchday 2,Matchday 3,...
Paris Saint-Germain,Liverpool,Bayern Munich,Barcelona,...
Arsenal,Inter,PSV,Sporting CP,...
...
```

### ⚽ Players Data with Fantasy Points (players)
```csv
playerId,name,rating,value,total points,goals,team,position,MD1,MD2,MD3,...
250076574,K. Mbappe,5.0,10.5,31,5,RMA,attackers,13,18,0,...
250103758,E. Haaland,5.0,10.5,19,3,MCI,attackers,6,13,0,...
250052469,M. Salah,4.5,10.5,11,1,LIV,midfielders,10,1,0,...
...
```

### 🎯 Personal Team Analysis (team)
```csv
playerId,name,rating,value,total points,position,team,is_captain,bench_position,starting_eleven
250016833,H. Kane,5.0,10.5,26.0,attackers,BAY,True,0,Yes
250076574,K. Mbappe,5.0,10.5,18.0,attackers,RMA,False,0,Yes
250099258,A. Lookman,0.5,7.0,2.0,midfielders,ATA,False,2,No
...
```

## 🚀 Quick Start

```bash
# Clone or download the project
cd /path/to/your/project

# Process fixtures to create opponents table
python main.py fixtures

# Process players data
python main.py players

# Get help
python main.py --help
```

## 📝 Installation

### ⚙️ Requirements
- **Python 3.8+** (Python 3.10+ recommended)
- **Internet connection** (to fetch live data from UEFA API)
- **AWS credentials** (for DynamoDB features - optional)
- **uv** (recommended) or pip for package management

### 📦 Dependencies
- **boto3>=1.26.0** - Required for DynamoDB export functionality
- **Standard library modules**: http.client, json, csv, logging, argparse, etc.

### 🚀 Quick Setup
```bash
# Using uv (recommended)
uv add boto3

# Or using pip
pip install -r requirements.txt

# Optional: Create virtual environment for isolation
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Test installation
./run.sh --help
```

### ☁️ AWS Setup (for DynamoDB features)
```bash
# Configure AWS credentials (one of the following):
# 1. AWS CLI
aws configure

# 2. Environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=eu-central-1

# 3. Credentials file (~/.aws/credentials)
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
region = eu-central-1
```

## Teams Supported

All 36 teams in the 2024-25 Champions League:
- Paris Saint-Germain, Liverpool, Arsenal, Manchester City, Chelsea
- Tottenham, Newcastle, Real Madrid, Barcelona, Atlético Madrid
- Athletic Club, Villarreal, Bayern Munich, Bayer Leverkusen
- Borussia Dortmund, Eintracht Frankfurt, Inter, Atalanta
- Juventus, Napoli, Marseille, Monaco, PSV, Ajax
- Benfica, Sporting CP, Club Brugge, Union Saint-Gilloise
- Galatasaray, Slavia Praha, Olympiacos, Copenhagen
- Bodø/Glimt, Kairat Almaty, Pafos, Qarabağ

## Error Handling

The application includes comprehensive error handling and logging:
- Network issues when fetching from UEFA API
- Data processing errors
- File writing permissions
- Graceful handling of interruptions (Ctrl+C)

## 🚀 Development

### Project Structure for Developers

```python
# Import examples for development
from src.api.client import UEFAApiClient
from src.core.team_mapper import TeamMapper
from src.core.processors import FixturesDataProcessor, PlayersDataProcessor
from src.exporters.csv_exporter import CSVExporter
```

### Testing

```bash
# Test with sample data (no API calls)
cd tests/
python test_paris.py

# This uses fixture_sample.json to test the opponents algorithm
# Perfect for development without hitting the live API
```

### Adding New Features

1. **New Data Source**: Add to `src/api/`
2. **New Processing Logic**: Add to `src/core/`
3. **New Export Format**: Add to `src/exporters/`
4. **New CLI Commands**: Extend `src/cli/app.py`

### Code Quality

```bash
# Optional: Install development tools
pip install black flake8 pytest

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Run tests (when you add them)
pytest tests/
```

## 🏗️ Architecture

The application uses a professional, modular architecture with clean separation of concerns:

```
backend/
├── src/                              # 🎯 Source code package
│   ├── api/                          # 🌐 External API communication
│   │   └── client.py                 # UEFAApiClient (with fantasy data)
│   ├── core/                         # 🧠 Core business logic
│   │   ├── team_mapper.py           # TeamMapper
│   │   ├── processors.py           # Data processors (with fantasy points)
│   │   └── team_analyzer.py        # TeamAnalyzer (NEW!)
│   ├── exporters/                   # 📊 Data export functionality
│   │   ├── csv_exporter.py         # CSVExporter (enhanced)
│   │   └── dynamodb_exporter.py    # DynamoDBExporter (NEW!)
│   └── cli/                         # 💻 Command-line interface
│       └── app.py                   # CLIApp (with team command)
├── tests/                           # 🧪 Test modules
├── json/                            # 📁 Sample and test data
├── run.sh                           # 🧹 Clean execution wrapper
├── requirements.txt                 # 📦 Dependencies
└── main.py                         # 🚀 Entry point
```

### 📁 **Core Components**

| Component | Location | Responsibility |
|-----------|----------|----------------|
| **UEFAApiClient** | `src/api/client.py` | HTTP communication with UEFA API + individual fantasy data |
| **TeamMapper** | `src/core/team_mapper.py` | Maps API team names to standardized names |
| **FixturesDataProcessor** | `src/core/processors.py` | Processes raw fixtures data from API |
| **OpponentsTableBuilder** | `src/core/processors.py` | Builds comprehensive opponents tables |
| **PlayersDataProcessor** | `src/core/processors.py` | Processes players + **fantasy points by matchday** |
| **TeamAnalyzer** | `src/core/team_analyzer.py` | **NEW**: Analyzes personal fantasy teams |
| **CSVExporter** | `src/exporters/csv_exporter.py` | Enhanced CSV export with dynamic columns |
| **DynamoDBExporter** | `src/exporters/dynamodb_exporter.py` | **NEW**: AWS DynamoDB cloud storage |
| **CLIApp** | `src/cli/app.py` | CLI with fixtures/players/**team** commands |

### ✨ **Architecture Benefits**

- ✅ **Separation of Concerns** - Each module has a single, clear responsibility
- ✅ **Easy Testing** - Individual components can be tested in isolation
- ✅ **Maintainable** - Changes to one component don't affect others
- ✅ **Extensible** - Easy to add new features or data sources
- ✅ **Professional** - Follows industry-standard Python project structure
- ✅ **Reusable** - Components can be imported and reused in other projects
- ✅ **Cloud Ready** - AWS DynamoDB integration for scalable data storage
- ✅ **Fantasy Focused** - Specialized features for fantasy football analysis

## 🆕 What's New

### 🎆 Recent Features Added
- **🎯 Fantasy Points by Matchday**: Individual MD1, MD2, MD3... fantasy points for each player
- **💾 DynamoDB Integration**: Export and store player data in AWS DynamoDB
- **🎮 Team Analysis**: Analyze your personal UEFA fantasy team lineup
- **📁 Team Export Options**: Export your fantasy team to CSV or DynamoDB
- **🔄 Clean Execution**: Wrapper script prevents .pyc file generation
- **🌐 Enhanced API Client**: Fetches individual player fantasy statistics
- **⚙️ Dynamic CSV**: Automatically detects and includes new columns (like MD fields)

### 🛠️ Technical Improvements
- **Enhanced Error Handling**: Better handling of players with no match data
- **Reduced Logging Verbosity**: Cleaner output with debug-level logging for details
- **Modular Design**: New TeamAnalyzer component for team-specific functionality
- **AWS Integration**: Complete DynamoDB setup with table creation and batch operations
- **Flexible CLI**: Support for multiple output formats and custom parameters

---

## 📝 CLI Commands Summary

### 🉐 Available Commands

| Command | Description | Example |
|---------|-------------|----------|
| `fixtures` | Process fixtures and create opponents table | `./run.sh fixtures -o opponents.csv` |
| `players csv` | Export players with fantasy points to CSV | `./run.sh players csv -o players.csv` |
| `players ddb` | Export players to DynamoDB | `./run.sh players ddb --region eu-west-1` |
| `team <guid>` | Analyze and export your fantasy team (CSV) | `./run.sh team <guid> -o my_team.csv` |
|| `team <guid> -e <table>` | Export your fantasy team to DynamoDB | `./run.sh team <guid> -e my-fantasy-team` |

### 🎁 Common Options

| Option | Short | Description | Example |
|--------|--------|-------------|----------|
| `--output` | `-o` | Custom output filename | `-o my_file.csv` |
| `--export-table` | `-e` | Export team to DynamoDB table | `-e my-fantasy-team` |
| `--table-name` | `-t` | Source DynamoDB table for player data | `-t my-players-table` |
| `--region` | | AWS region for DynamoDB | `--region us-east-1` |
| `--matchday` | `-m` | Specific matchday for team | `-m 3` |
| `--json-fallback` | `-j` | JSON fallback file | `-j backup.json` |
| `--help` | `-h` | Show command help | `--help` |

---

## 🔧 Troubleshooting

### 🚑 Common Issues

**"No fixtures data retrieved"**
```bash
# Check your internet connection
# The UEFA API might be temporarily unavailable
# Try again in a few minutes
```

**"AWS credentials not found" (DynamoDB features)**
```bash
# Set up AWS credentials using one of these methods:
aws configure                          # AWS CLI method
export AWS_ACCESS_KEY_ID=your_key     # Environment variables
# Or create ~/.aws/credentials file
```

**"Player not found in DB" warnings**
```bash
# This is normal - some players haven't played yet
# They get default 0 points for all matchdays
# No action needed
```

**"HTTP 403: Forbidden" for team analysis**
```bash
# Your UEFA session might have expired
# Use the JSON fallback option:
./run.sh team <guid> --json-fallback json/my_team.json
```

**Import errors after updates**
```bash
# Make sure you're running from the project root directory
cd /path/to/your/project
./run.sh --help

# Reinstall dependencies if needed
uv add boto3
```

**CSV file not found**
```bash
# Check current directory - CSV files are created in the same directory
ls -la *.csv

# Use absolute paths for custom output locations
./run.sh fixtures -o /path/to/output/my_fixtures.csv
```

### Debugging

```bash
# Enable verbose logging (modify src/cli/app.py)
# Change logging level from INFO to DEBUG
```

---

## 🤝 Contributing

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow the modular architecture**:
   - API changes → `src/api/`
   - Business logic → `src/core/`
   - Export features → `src/exporters/`
   - CLI improvements → `src/cli/`
4. **Add tests** in the `tests/` directory
5. **Submit a pull request**

### Code Style
- Follow PEP 8 conventions
- Use type hints where possible
- Add docstrings to classes and functions
- Keep functions focused and single-purpose

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- UEFA for providing the fantasy football API
- Python community for excellent standard library modules
- All contributors who help improve this project
