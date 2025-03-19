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
│   ├── core/
│   │   ├── db/                     # Database package
│   │   │   ├── __init__.py         # Package exports
│   │   │   ├── common.py           # Shared database utilities
│   │   │   ├── schema.py           # Database schema definitions
│   │   │   ├── pitcher_utils.py    # Pitcher data storage/retrieval
│   │   │   └── team_utils.py       # Team data storage/retrieval
│   │   ├── db_manager.py           # High-level database interface
│   │   ├── db_utils.py             # Facade importing from db package 
│   │   ├── gamelog_scraper.py      # Scraper for pitcher game logs
│   │   ├── player_utils.py         # Player data utilities
│   │   └── team_stats_scraper.py   # Scraper for team batting stats
│   ├── csv/
│   │   ├── starting_pitchers_ids.csv  # Main input file with player IDs
│   │   └── test_ids.csv               # Test input file with few player IDs
│   ├── docs/
│   │   └── README_QUERY.md            # Guide for querying the database
│   └── scripts/
│       ├── gamelog_scrape.py     # Script for scraping pitcher game logs
│       └── scrape_team_stats.py  # Script for scraping team batting stats
└── README.md                     # This file
```

## Database Structure

The database organization has been improved through modularization:

- `db/schema.py`: Contains database table definitions and creation logic
- `db/pitcher_utils.py`: Functions for storing and retrieving pitcher data
- `db/team_utils.py`: Functions for storing and retrieving team statistics
- `db/common.py`: Shared utilities and column mapping definitions

The original `db_utils.py` now acts as a facade that maintains backward compatibility.

## Usage

### Scraping Pitcher Game Logs

The `gamelog_scrape.py` script handles scraping pitcher game logs:

```bash
# Create a database using the full list of pitchers
uv run src/scripts/gamelog_scrape.py

# Test with a smaller list
uv run src/scripts/gamelog_scrape.py --test

# Specify a custom input file
uv run src/scripts/gamelog_scrape.py --input-file path/to/ids.csv

# Limit the number of players to scrape
uv run src/scripts/gamelog_scrape.py --limit 10

# Recreate the database (will delete existing data)
uv run src/scripts/gamelog_scrape.py --reset-db

# Specify which years to scrape
uv run src/scripts/gamelog_scrape.py --years 2021 2022 2023

# Specify database path
uv run src/scripts/gamelog_scrape.py --db-path my_database.db

# Enable verbose logging
uv run src/scripts/gamelog_scrape.py --verbose
```

### Scraping Team Batting Stats

The `scrape_team_stats.py` script handles scraping team batting statistics:

```bash
# Scrape team batting stats for the current year
uv run src/scripts/scrape_team_stats.py

# Scrape team batting stats for specific years
uv run src/scripts/scrape_team_stats.py --years 2021 2022 2023

# Specify database path
uv run src/scripts/scrape_team_stats.py --db-path my_database.db

# Enable verbose logging
uv run src/scripts/scrape_team_stats.py --verbose
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
