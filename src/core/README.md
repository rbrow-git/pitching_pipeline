# Core Module

This directory contains the core business logic for the Baseball Pitching Pipeline.

## Submodules

### Database (`db/`)

The `db` package contains all database-related functionality:

- `column_mapping.py`: Shared utilities and column mapping definitions
- `schema.py`: Database schema definitions
- `pitcher_utils.py`: Functions for storing and retrieving pitcher data
- `database_manager.py`: Unified database interface class
- `team_utils.py`: Functions for storing and retrieving team statistics

### Scrapers

- `gamelog_scraper.py`: Functions for scraping pitcher game logs from Baseball Reference
- `team_stats_scraper.py`: Functions for scraping team batting statistics from Baseball Reference

### Utilities

- `player_utils.py`: Utilities for loading and processing player data
- `scraper_manager.py`: High-level functions for database operations (uses the `db` package)

## Architecture

The core module follows a modular architecture:

1. **Scrapers**: Fetch data from external sources
2. **Database**: Store and retrieve data
3. **Utilities**: Process and transform data

## Dependencies

The core module depends on:

- `pandas`: For data manipulation
- `scrapling`: For web scraping
- Standard library modules: `sqlite3`, `logging`, etc.

## Example Usage

```python
from src.core.gamelog_scraper import scrape_player
from src.core.db import db_manager

# Scrape data for a player
data, name = scrape_player("degroja01")

# Store the data
db_manager.store_pitcher_data(data, "degroja01", name)
``` 