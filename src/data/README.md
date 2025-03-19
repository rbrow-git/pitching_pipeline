# Input Data Files

This directory contains CSV files with player IDs and other input data required for the Baseball Pitching Pipeline.

## Files

- `starting_pitchers_ids.csv`: The main list of pitcher IDs to scrape from Baseball Reference
- `test_ids.csv`: A smaller list of pitcher IDs for testing purposes

## File Format

The input CSV files should have a column named `player_id` containing Baseball Reference player IDs:

```
player_id
snellbl01
flaheja01
degroja01
...
```

## Usage

These files are used by the CLI commands:

```bash
# Use the main list of pitchers
uv run src/cli/main.py pitchers

# Use the test list with fewer pitchers
uv run src/cli/main.py pitchers --test

# Use a custom input file
uv run src/cli/main.py pitchers --input-file path/to/your/ids.csv
```

## Adding New Players

To add new players:
1. Find the player's ID on Baseball Reference (typically in the URL of their player page)
2. Add the ID to the CSV file in a new row
3. Run the CLI command to scrape data for the new players 