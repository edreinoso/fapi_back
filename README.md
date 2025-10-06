# UEFA Champions League Fantasy Data Processor

A command-line application to fetch and process UEFA Champions League fantasy football data, including player statistics and team fixtures with opponent tables.

## Features

- **🏆 Fixtures Processing**: Creates an opponents table showing who each team plays in each matchday
- **⚽ Players Processing**: Fetches and processes player statistics and data
- **📊 CSV Export**: Exports data to CSV files for easy analysis
- **🎯 Team Name Mapping**: Handles team name variations between API and standard names

## Usage

### Basic Commands

```bash
# Show help
python main.py --help

# Process fixtures and create opponents table
python main.py fixtures

# Process players data
python main.py players
```

### Advanced Usage

```bash
# Specify custom output filename for fixtures
python main.py fixtures --output my_opponents.csv
python main.py fixtures -o my_opponents.csv

# Specify custom output filename for players
python main.py players --output my_players.csv
python main.py players -o my_players.csv

# Get help for specific commands
python main.py fixtures --help
python main.py players --help
```

## Output Files

### Fixtures Command
- **Default**: `uefa_opponents_table.csv`
- **Format**: Teams as rows, matchdays as columns, opponents as cell values
- **Content**: Who each team plays in each matchday of the Champions League

### Players Command
- **Default**: `players_data.csv`
- **Content**: Player statistics including:
  - Name, rating, value, points
  - Goals, assists, minutes played
  - Position, team, selection percentage
  - And more...

## Example Output

### Opponents Table (fixtures)
```csv
Team,Matchday 1,Matchday 2,Matchday 3,...
Paris Saint-Germain,Liverpool,Bayern Munich,Barcelona,...
Arsenal,Inter,PSV,Sporting CP,...
...
```

### Players Data (players)
```csv
name,rating,value,total points,goals,team,position,...
Kylian Mbappé,95,12.5,45,8,PSG,attackers,...
Erling Haaland,94,12.0,52,12,MCI,attackers,...
...
```

## Requirements

- Python 3.6+
- Internet connection (to fetch live data from UEFA API)

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

## Development

### Test with Sample Data
```bash
# Test the algorithm with sample fixture data for Paris Saint-Germain
python test_paris.py
```

This will use the `fixture_sample.json` file to test the opponents algorithm without making API calls.

## Architecture

The application now uses a clean, modular architecture with separated concerns:

### 📁 **Core Classes**

- **`UEFAApiClient`** (`uefa_api_client.py`) - Handles all API communication with UEFA
- **`TeamMapper`** (`team_mapper.py`) - Maps API team names to standardized names
- **`FixturesDataProcessor`** (`data_processors.py`) - Processes raw fixtures data
- **`OpponentsTableBuilder`** (`data_processors.py`) - Builds opponents tables from fixtures
- **`PlayersDataProcessor`** (`data_processors.py`) - Processes raw players data
- **`CSVExporter`** (`csv_exporter.py`) - Handles all CSV export functionality
- **`CLIApp`** (`cli_app.py`) - Main application controller and CLI interface

### 🔧 **Entry Points**

- **`main.py`** - Legacy entry point for backward compatibility
- **`cli_app.py`** - Main modular CLI application
- **`test_paris.py`** - Test script using sample data

### 🏗️ **Benefits of New Architecture**

- **Separation of Concerns** - Each class has a single responsibility
- **Easy Testing** - Individual components can be tested in isolation
- **Maintainability** - Changes to one component don't affect others
- **Extensibility** - Easy to add new features or data sources
- **Reusability** - Components can be reused in other applications
