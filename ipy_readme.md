# Baseball Reference Pitching Game Log Scraper

This script scrapes pitching game logs from Baseball Reference for a specified list of players and years, cleans the data, and stores it in an SQLite database.

## Dependencies

- `scrapling`: For handling web scraping with stealth.
- `pandas`: For data manipulation and storage in DataFrames.
- `beautifulsoup4`: For parsing HTML content.
- `sqlite3`: For storing data in an SQLite database.
- `asyncio`: For handling asynchronous operations.
- `nest_asyncio`: To allow asyncio to run in Jupyter Notebook.

To install the necessary dependencies, use `uv`:

```bash
uv venv .venv
source .venv/bin/activate
uv sync
```

## Usage

1.  **Prepare a CSV file:**
    Create a CSV file (`test_ids.csv` by default) containing a column named `player_id` with the Baseball Reference player IDs you want to scrape.

2.  **Run the script:**
    Execute the script in a Jupyter Notebook environment.

    ```python
    import asyncio
    import nest_asyncio

    # Apply nest_asyncio to allow asyncio to run in Jupyter Notebook
    nest_asyncio.apply()

    # Filepath to your CSV file (update this if needed)
    csv_filepath = "test_ids.csv"  # Adjust if it's in a different directory

    # Run the async function in the event loop
    asyncio.run(scrape_all_players(csv_filepath))
    ```

## Functions

### `scrape_year(player_id, year)`

Scrapes pitching game logs for a player for a specific year from Baseball Reference.

-   **Parameters:**
    -   `player_id` (str): Baseball Reference player ID.
    -   `year` (int): Year to scrape.
-   **Returns:**
    -   `tuple`: A tuple containing a pandas DataFrame with the game logs and the player name.

### `player_scrape(player_id)`

Scrapes and combines pitching data for a player from 2021 to 2024.

-   **Parameters:**
    -   `player_id` (str): Baseball Reference player ID.
-   **Returns:**
    -   `pandas.DataFrame`: A DataFrame containing combined game logs for the specified years.

### `cleanse_pitcher_game_logs(df)`

Cleans and transforms the scraped game log data.

-   **Parameters:**
    -   `df` (pandas.DataFrame): DataFrame containing raw game log data.
-   **Returns:**
    -   `pandas.DataFrame`: Cleaned DataFrame with renamed columns and dummy variables for the road indicator.

### `save_pitcher_logs(df, db_path="baseball.db")`

Saves the cleaned game logs and player information to an SQLite database.

-   **Parameters:**
    -   `df` (pandas.DataFrame): DataFrame containing cleaned game log data.
    -   `db_path` (str, optional): Path to the SQLite database file. Defaults to `"baseball.db"`.

### `scrape_all_players(filepath)`

Orchestrates the scraping, cleaning, and saving of data for all players listed in the provided CSV file.

-   **Parameters:**
    -   `filepath` (str): Path to the CSV file containing player IDs.

## Data Cleaning

The `cleanse_pitcher_game_logs` function performs the following cleaning steps:

-   Renames columns using a predefined mapping (`rename_map`).
-   Drops unnecessary columns (`Dec`, `IR`, `IS`, `Unk`, `DFS(DK)`, `DFS(FD)`, `Entered`, `Exited`,`Rslt`,`Inngs`).
-   Converts the `road_indicator` column to dummy variables.
-   Filters out invalid rows based on `team_id`.
-   Ensures `player_id`, `name`, and `year` are the first three columns.

## Database Storage

The `save_pitcher_logs` function saves the data into two tables:

-   `pitching_gamelogs`: Contains the cleaned game log data.
-   `scraped_players`: Contains unique player IDs and names.

## Error Handling

The script includes error handling for web scraping requests and data processing. It uses logging to provide information about the scraping process, including any errors or warnings encountered.