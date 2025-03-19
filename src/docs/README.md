# Documentation

This directory contains documentation for the Baseball Pitching Pipeline.

## Contents

- `README_QUERY.md`: Guide for querying the database with example SQL queries
- `LOGGING.md`: Guidelines and best practices for using the logging system

## Database Schema

The database schema is defined in `src/core/db/schema.py` and includes the following tables:

- `pitching_gamelogs`: Contains pitcher game logs with performance statistics
- `players`: Contains player metadata (ID, name, last updated timestamp)
- `team_stats`: Contains team batting statistics

## Getting Started with Querying

To query the database:

1. First, create the database by running one of the CLI commands:
   ```bash
   uv run src/cli/main.py pitchers
   uv run src/cli/main.py teams
   ```

2. Then, use your favorite SQLite client to open the database file (default: `baseball.db`)

3. Refer to the README_QUERY.md for example queries

## Logging Configuration

The application uses a centralized logging configuration that can be controlled in several ways:

1. Command-line flag: Add `--verbose` or `-v` to any command to enable detailed logging
   ```bash
   uv run src/cli/main.py pitchers --verbose
   ```

2. Environment variables:
   ```bash
   # Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   export BASEBALL_LOG_LEVEL="INFO"
   
   # Enable verbose mode
   export BASEBALL_VERBOSE=1
   ```

3. See `LOGGING.md` for detailed information on logging best practices

## Adding Documentation

When adding new features or modifying existing ones, please update the documentation accordingly:

1. Add SQL examples for new tables or columns
2. Document any changes to the database schema
3. Update usage examples as needed 