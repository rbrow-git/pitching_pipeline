# Baseball Pitching Pipeline

A tool for scraping MLB pitcher statistics and team batting statistics, and storing them in a SQLite database.

## Overview

This project scrapes various baseball statistics from Baseball Reference and stores them in a structured SQLite database for analysis. The main components are:

1. **Pitcher Game Logs**: Scrape individual pitcher game logs from player pages
2. **Team Batting Stats**: Scrape team batting statistics

## Project Structure

```
pitching_pipeline/
├── src/
│   ├── cli/                     # Unified command-line interface
│   │   ├── __init__.py
│   │   └── main.py              # Main CLI entry point with subcommands
│   ├── core/                    # Core business logic
│   │   ├── db/                  # Database package
│   │   │   ├── __init__.py
│   │   │   ├── common.py        # Shared database utilities
│   │   │   ├── schema.py        # Database schema definitions
│   │   │   ├── pitcher_utils.py # Pitcher data storage/retrieval
│   │   │   ├── team_utils.py    # Team data storage/retrieval
│   │   │   └── database_manager.py # Unified database interface
│   │   ├── db_manager.py        # High-level database operations
│   │   ├── gamelog_scraper.py   # Scraper for pitcher game logs
│   │   ├── player_utils.py      # Player data utilities
│   │   └── team_stats_scraper.py # Scraper for team batting stats
│   ├── data/                    # Input data files
│   │   ├── starting_pitchers_ids.csv  # Main input file with player IDs
│   │   └── test_ids.csv              # Test input file with few player IDs
│   ├── docs/                    # Documentation
│   │   └── README_QUERY.md      # Guide for querying the database
│   └── utils/                   # General-purpose utility functions
│       ├── __init__.py
│       └── README.md            # Documentation for utilities
└── README.md                    # This file
```

## Getting Started for Non-Python Users

If you're new to Python, here's a step-by-step guide to help you use this tool:

### 1. Prerequisites

This project uses the `uv` package manager instead of pip. Make sure you have:

- Python 3.6 or higher installed
- `uv` package manager installed
- Git installed (to clone the repository)

### 2. Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/pitching_pipeline.git
cd pitching_pipeline

# 2. Install the required dependencies
uv add pandas
uv add scrapling
```

### 3. Basic Usage

The project has a unified command-line interface that makes it easy to run different operations:

```bash
# Scrape pitcher game logs
uv run src/cli/main.py pitchers

# Scrape team batting stats
uv run src/cli/main.py teams
```

### 4. Process Flow Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  Input Data  │       │   Scraping   │       │   Database   │       │    Query     │
│  (CSV files) │ ──────▶  Functions   │ ──────▶   Creation   │ ──────▶   Results    │
│  src/data/   │       │  src/core/   │       │  src/core/db │       │ (SQL queries)│
└──────────────┘       └──────────────┘       └──────────────┘       └──────────────┘
```

### 5. Understanding the Folders

- `src/cli/`: Contains the unified command-line interface
- `src/core/`: Contains the core business logic for scraping and database operations
- `src/data/`: Contains input CSV files with player IDs
- `src/docs/`: Contains documentation for using the database
- `src/utils/`: Contains general-purpose utility functions

## Usage

### Scraping Pitcher Game Logs

Use the unified CLI with the `pitchers` subcommand:

```bash
# Create a database using the full list of pitchers
uv run src/cli/main.py pitchers

# Test with a smaller list
uv run src/cli/main.py pitchers --test

# Specify a custom input file
uv run src/cli/main.py pitchers --input-file path/to/ids.csv

# Limit the number of players to scrape
uv run src/cli/main.py pitchers --limit 10

# Recreate the database (will delete existing data)
uv run src/cli/main.py pitchers --reset-db

# Specify which years to scrape
uv run src/cli/main.py pitchers --years 2021 2022 2023

# Specify database path
uv run src/cli/main.py pitchers --db-path my_database.db

# Enable verbose logging
uv run src/cli/main.py pitchers --verbose
```

### Scraping Team Batting Stats

Use the unified CLI with the `teams` subcommand:

```bash
# Scrape team batting stats for the current year
uv run src/cli/main.py teams

# Scrape team batting stats for specific years
uv run src/cli/main.py teams --years 2021 2022 2023

# Specify database path
uv run src/cli/main.py teams --db-path my_database.db

# Enable verbose logging
uv run src/cli/main.py teams --verbose
```

## Input File Format

The player ID input CSV file should contain a column named `player_id` with Baseball Reference player IDs:

```
player_id
snellbl01
flaheja01
degroja01
...
```

## Querying the Database

After creating the database, you can query it using SQLite directly. See the [Database Query Guide](src/docs/README_QUERY.md) for examples and reference SQL queries.

## Development

This project uses the uv package manager instead of pip. To install dependencies:

```bash
uv add pandas
uv add scrapling
```

## Extending the Pipeline

### Adding a New Tool

Follow these steps to add a new scraping tool that creates a new table in the database:

1. **Define the Database Schema**
   - Add your new table definition in `src/core/db/schema.py`
   - Define column mappings in `src/core/db/common.py`

   ```python
   # In schema.py
   cursor.execute("""
   CREATE TABLE IF NOT EXISTS your_new_table (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       some_field TEXT NOT NULL,
       another_field INTEGER,
       ...
       UNIQUE(some_field, another_field)
   )
   """)
   
   # In common.py
   new_table_column_mapping = {
       'scraped_field_name': 'database_column_name',
       'another_scraped_field': 'another_column',
       ...
   }
   ```

2. **Create a Scraper Module**
   - Add a new file in `src/core/` (e.g., `your_scraper.py`)
   - Implement the scraping logic using the `scrapling` library

   ```python
   # Example scraper function
   def scrape_your_data(param1, param2=None):
       """Scrape data for your new feature"""
       # Implement scraping logic
       # Return DataFrame with results
       return df
   ```

3. **Create Database Utilities**
   - Add a new file in `src/core/db/` (e.g., `your_utils.py`)
   - Implement functions to store and retrieve data

   ```python
   def store_your_data(df, db_path="baseball.db"):
       """Store scraped data into the database"""
       # Implement database storage logic
       return success
   
   def get_your_data(param=None, db_path="baseball.db"):
       """Retrieve your data from the database"""
       # Implement query logic
       return df
   ```

4. **Update the Database Manager**
   - Add your new functions to `src/core/db/database_manager.py`
   - Update the exports in `src/core/db/__init__.py`

   ```python
   # In database_manager.py
   def store_your_data(self, df):
       """Store your data in the database"""
       return store_your_data(df, self.db_path)
   
   def get_your_data(self, param=None):
       """Retrieve your data from the database"""
       return get_your_data(param, self.db_path)
   ```

5. **Add High-Level Functions**
   - Add high-level functions to `src/core/db_manager.py`

   ```python
   def scrape_and_store_your_data(param1, param2, db_path="baseball.db"):
       """Scrape and store your data"""
       df = scrape_your_data(param1, param2)
       if df is not None and not df.empty:
           return store_your_data(df, db_path)
       return False
   ```

6. **Add CLI Support**
   - Update `src/cli/main.py` to add a new subcommand

   ```python
   # In the main() function
   parser_your_tool = subparsers.add_parser("your_tool", help="Description of your tool")
   parser_your_tool.add_argument("--param1", required=True, help="Description of param1")
   parser_your_tool.add_argument("--param2", type=int, help="Description of param2")
   parser_your_tool.add_argument("--db-path", type=str, default="baseball.db", help="Path to SQLite database")
   parser_your_tool.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
   parser_your_tool.set_defaults(func=handle_your_tool)
   
   # Add the handler function
   def handle_your_tool(args):
       """Handle the 'your_tool' subcommand"""
       db_path = initialize_database(args.db_path)
       success = scrape_and_store_your_data(args.param1, args.param2, db_path)
       if success:
           logger.info("✅ Your tool completed successfully")
           return 0
       else:
           logger.error("❌ Your tool failed")
           return 1
   ```

7. **Update Documentation**
   - Add usage examples to the README.md
   - Document the new table schema and its purpose

### Example: Adding a Player Career Stats Tool

Here's a concrete example of how you might add a new tool to scrape player career statistics:

```python
# 1. In schema.py
cursor.execute("""
CREATE TABLE IF NOT EXISTS career_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL,
    seasons INTEGER,
    games INTEGER,
    wins INTEGER,
    losses INTEGER,
    career_era REAL,
    UNIQUE(player_id)
)
""")

# 2. In your_scraper.py
def scrape_career_stats(player_id):
    """Scrape career statistics for a player"""
    # Implementation
    return df

# 3. In CLI
parser_career = subparsers.add_parser("career", help="Scrape player career statistics")
parser_career.add_argument("--player-id", required=True, help="Player ID to scrape")
parser_career.set_defaults(func=handle_career)

def handle_career(args):
    """Handle career stats command"""
    success = scrape_and_store_career_stats(args.player_id, args.db_path)
    return 0 if success else 1
```

To use your new tool:

```bash
uv run src/cli/main.py your_tool --param1 value --param2 value
```
