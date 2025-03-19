# Command Line Interface

This directory contains the unified command-line interface for the Baseball Pitching Pipeline.

## Structure

- `__init__.py`: Package initialization file
- `main.py`: Main CLI entry point with subcommands for different operations

## Usage

The CLI provides two main subcommands:

### `pitchers` - Scrape pitcher game logs

```bash
# Basic usage with default options
uv run src/cli/main.py pitchers

# Using the test dataset
uv run src/cli/main.py pitchers --test

# Specifying custom options
uv run src/cli/main.py pitchers --years 2021 2022 2023 --db-path custom.db --limit 10
```

### `teams` - Scrape team batting statistics

```bash
# Basic usage with default options (current year)
uv run src/cli/main.py teams

# Specifying years to scrape
uv run src/cli/main.py teams --years 2021 2022 2023
```

## Full Command Reference

Run with `--help` to see all available options:

```bash
uv run src/cli/main.py --help
uv run src/cli/main.py pitchers --help
uv run src/cli/main.py teams --help
``` 