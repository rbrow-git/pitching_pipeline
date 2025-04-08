import statsapi
import pandas as pd
from pprint import pprint
import sys

# --- Configuration ---
PLAYER_ID = 471911 # Carlos Carrasco
SEASONS = [2023, 2024, 2025]
STAT_TYPE = 'gameLog'
STAT_GROUP = 'pitching'
OUTPUT_FILENAME = f"player_{PLAYER_ID}_pitching_logs_{'_'.join(map(str, SEASONS))}.csv"
# --- End Configuration ---

def fetch_game_logs(person_id, season, stat_type, stat_group):
    """Fetches game logs for a specific player, season, stat type, and group."""
    hydrate_string = f"stats(group=[{stat_group}],type={stat_type},season={season}),currentTeam"

    print(f"Fetching {season} {stat_type} stats for group '{stat_group}' for player ID: {person_id}...")
    print(f"Hydrate string: {hydrate_string}")

    try:
        # Call statsapi.get directly for the 'person' endpoint
        api_response = statsapi.get(
            endpoint='person',
            params={'personId': person_id, 'hydrate': hydrate_string}
        )
        print(f"API call for {season} successful.")
        return api_response
    except Exception as e:
        print(f"An error occurred during the API call for {season}: {e}")
        return None

def process_response(api_response, person_id, season, stat_type, stat_group):
    """Processes the API response and extracts game logs into a DataFrame."""
    if not api_response or 'people' not in api_response or not api_response['people']:
        print(f"Failed to process data for {season}: Invalid response structure.")
        if api_response:
            print("API Response:")
            pprint(api_response)
        return None

    person_info = api_response['people'][0]
    game_logs_split = None

    if 'stats' in person_info:
        for stat_entry in person_info['stats']:
            if (stat_entry.get('type', {}).get('displayName') == stat_type and
                stat_entry.get('group', {}).get('displayName') == stat_group and
                stat_entry.get('splits') and
                (not stat_entry['splits'] or str(stat_entry['splits'][0].get('season')) == str(season))):
                game_logs_split = stat_entry['splits']
                break

    if game_logs_split:
        df_season = pd.json_normalize(game_logs_split)
        print(f"Successfully processed {len(df_season)} game logs for {season}.")
        return df_season
    else:
        print(f"Could not find '{stat_type}' stats for group '{stat_group}' and season {season} in the response.")
        # Optionally print the response structure if logs are missing for debugging
        # print("Response structure received:")
        # pprint(api_response)
        return None

def main():
    """Main function to fetch, process, and combine data for multiple seasons."""
    all_season_dfs = []

    # Ensure the statsapi directory is importable
    # This assumes the script is run from the parent directory of toddrob99-mlb-statsapi
    # Or that the toddrob99-mlb-statsapi directory is in the Python path
    print("Checking if statsapi module is accessible...")
    try:
        _ = statsapi.ENDPOINTS # Try accessing something from the module
        print("statsapi module found.")
    except AttributeError:
         print("Error: Cannot find the 'statsapi' module.")
         print("Please ensure the 'toddrob99-mlb-statsapi' directory is in the same directory as this script or in your PYTHONPATH.")
         sys.exit(1)
    except ImportError:
        print("Error: Could not import the 'statsapi' module.")
        print("Please ensure the 'toddrob99-mlb-statsapi' directory is in the same directory as this script or in your PYTHONPATH.")
        sys.exit(1)


    for year in SEASONS:
        response = fetch_game_logs(PLAYER_ID, year, STAT_TYPE, STAT_GROUP)
        if response:
            df = process_response(response, PLAYER_ID, year, STAT_TYPE, STAT_GROUP)
            if df is not None and not df.empty:
                # Add a season column for clarity when combining
                df['season_queried'] = year
                all_season_dfs.append(df)
        print("-" * 30) # Separator between seasons

    if not all_season_dfs:
        print("No game log data found for any of the specified seasons.")
        return

    print("\nCombining dataframes...")
    final_df = pd.concat(all_season_dfs, ignore_index=True)

    print("\nCombined DataFrame Info:")
    final_df.info()

    print(f"\nTotal game logs fetched: {len(final_df)}")
    print("\nCombined DataFrame Head:")
    print(final_df.head())

    # --- Optional: Save to CSV ---
    try:
        final_df.to_csv(OUTPUT_FILENAME, index=False)
        print(f"\nSuccessfully saved combined data to '{OUTPUT_FILENAME}'")
    except Exception as e:
        print(f"\nError saving data to CSV: {e}")
    # --- End Optional ---

if __name__ == "__main__":
    main()