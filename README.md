# Baseball Reference Pitcher Data Scraper

A modular tool for scraping MLB pitcher game logs from Baseball Reference and storing them in a SQLite database.

## Features

- Scrape pitching game logs for individual or multiple MLB pitchers
- Store data in a SQLite database for easy querying and analysis
- Modular design with separate components for scraping, data storage, and utilities
- Command-line interface with flexible options
- Handles connection errors and retries with different fetching methods

## Requirements

- Python 3.9+
- Required Python packages:
  - scrapling
  - pandas
  - argparse

## Installation

1. Clone this repository or download the source code
2. Install dependencies:

```bash
uv add scrapling pandas argparse
uv run scrapling install  # Install browser dependencies
```

## Usage

### Basic Usage

Scrape data for a single player:

```bash
uv run python main.py --player-id snellbl01
```

Scrape data for multiple players from a CSV file:

```bash
uv run python main.py --players-file starting_pitchers_ids.csv
```

### Advanced Options

Specify years to scrape:

```bash
uv run python main.py --player-id snellbl01 --years 2021 2022 2023
```

Specify database path:

```bash
uv run python main.py --player-id snellbl01 --db-path my_baseball_data.db
```

Limit number of players to process from a file:

```bash
uv run python main.py --players-file starting_pitchers_ids.csv --max-players 10
```

## Project Structure

- `main.py`: Entry point with command-line interface
- `scraper.py`: Functions for scraping data from Baseball Reference
- `db_utils.py`: Database operations for storing and retrieving data
- `utils.py`: Utility functions for data loading and manipulation

## Database Schema

The SQLite database contains the following tables:

- `pitching_gamelogs`: Stores individual game statistics for pitchers
- `players`: Tracks which players have been scraped and when

## Examples

### Scrape a single player and print results

```python
from scraper import scrape_player
from db_utils import create_database, store_pitcher_data

# Scrape data for Blake Snell for 2021-2023
df = scrape_player('snellbl01', [2021, 2022, 2023])

# Store in database
create_database('baseball.db')
store_pitcher_data(df, 'snellbl01', 'baseball.db')
```

### Query data from the database

```python
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('baseball.db')

# Query all games with 10+ strikeouts
query = """
SELECT player_id, year, game_date, strikeouts 
FROM pitching_gamelogs 
WHERE strikeouts >= 10
ORDER BY strikeouts DESC
"""

# Load into pandas DataFrame
results = pd.read_sql_query(query, conn)
print(results)
```

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
