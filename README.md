# ⚽ UEFA Champions League Fantasy Data Processor

A professional command-line application to fetch and process UEFA Champions League fantasy football data, including player statistics and team fixtures with opponent tables.

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

- **🏆 Fixtures Processing**: Creates comprehensive opponents tables showing who each team plays in each matchday
- **⚽ Players Processing**: Fetches and processes detailed player statistics and performance data
- **📊 CSV Export**: Exports data to clean, well-formatted CSV files for analysis
- **🎯 Team Name Mapping**: Handles team name variations between API and standard names intelligently
- **🏗️ Modular Architecture**: Professional code organization with separation of concerns
- **🔧 Zero Dependencies**: Uses only Python standard library - no external packages required!
- **💻 CLI Interface**: User-friendly command-line interface with helpful error messages
- **📝 Comprehensive Logging**: Detailed logging for debugging and monitoring

## 💻 Usage

### Basic Commands

```bash
# Show main help
./run.sh --help                    # Using clean wrapper script
# OR
uv run python main.py --help       # Direct execution

# Process fixtures and create opponents table
./run.sh fixtures
# → Creates: uefa_opponents_table.csv

# Process players data to CSV (default)
./run.sh players
# → Creates: players_data.csv

# Process players data to DynamoDB
./run.sh players ddb
# → Creates/updates: uefa-players table in DynamoDB
```

### Advanced Usage

```bash
# Custom output filenames
python main.py fixtures --output my_opponents_2024.csv
python main.py fixtures -o champions_league_fixtures.csv

python main.py players --output player_stats_oct2024.csv
python main.py players -o uefa_players.csv

# Get detailed help for specific commands
python main.py fixtures --help
python main.py players --help
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

### Requirements
- **Python 3.6+** (Python 3.8+ recommended)
- **Internet connection** (to fetch live data from UEFA API)
- **No external dependencies!** 🎉

### Setup
```bash
# No installation needed! Just run:
python main.py --help

# Optional: Create virtual environment for isolation
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
│   │   └── client.py                 # UEFAApiClient
│   ├── core/                         # 🧠 Core business logic
│   │   ├── team_mapper.py           # TeamMapper
│   │   └── processors.py           # Data processors
│   ├── exporters/                   # 📊 Data export functionality
│   │   └── csv_exporter.py         # CSVExporter
│   └── cli/                         # 💻 Command-line interface
│       └── app.py                   # CLIApp
├── tests/                           # 🧪 Test modules
└── main.py                         # 🚀 Entry point
```

### 📁 **Core Components**

| Component | Location | Responsibility |
|-----------|----------|----------------|
| **UEFAApiClient** | `src/api/client.py` | Handles all HTTP communication with UEFA API |
| **TeamMapper** | `src/core/team_mapper.py` | Maps API team names to standardized names |
| **FixturesDataProcessor** | `src/core/processors.py` | Processes raw fixtures data from API |
| **OpponentsTableBuilder** | `src/core/processors.py` | Builds comprehensive opponents tables |
| **PlayersDataProcessor** | `src/core/processors.py` | Processes player statistics and performance data |
| **CSVExporter** | `src/exporters/csv_exporter.py` | Handles all CSV export functionality |
| **CLIApp** | `src/cli/app.py` | Main application controller and CLI interface |

### ✨ **Architecture Benefits**

- ✅ **Separation of Concerns** - Each module has a single, clear responsibility
- ✅ **Easy Testing** - Individual components can be tested in isolation
- ✅ **Maintainable** - Changes to one component don't affect others
- ✅ **Extensible** - Easy to add new features or data sources
- ✅ **Professional** - Follows industry-standard Python project structure
- ✅ **Reusable** - Components can be imported and reused in other projects

---

## 🔧 Troubleshooting

### Common Issues

**"No fixtures data retrieved"**
```bash
# Check your internet connection
# The UEFA API might be temporarily unavailable
# Try again in a few minutes
```

**Import errors after restructuring**
```bash
# Make sure you're running from the project root directory
cd /path/to/your/project
python main.py --help
```

**CSV file not found**
```bash
# Check current directory - CSV files are created in the same directory
ls -la *.csv

# Use absolute paths for custom output locations
python main.py fixtures -o /path/to/output/my_fixtures.csv
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
