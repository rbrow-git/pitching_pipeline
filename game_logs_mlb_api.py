import statsapi
import pandas as pd
from pprint import pprint
import sys
import datetime # Added for filename

# Import the function from the other script
from fetch_probable_pitchers_api import get_probable_pitchers_today

# --- Configuration ---
# PLAYER_ID removed, will be fetched dynamically
SEASONS = [2023, 2024, 2025]
STAT_TYPE = 'gameLog'
STAT_GROUP = 'pitching'
# Updated filename logic
today_date_str = datetime.date.today().strftime("%Y%m%d")
OUTPUT_FILENAME = f"probable_pitchers_game_logs_{today_date_str}.csv"
# --- End Configuration ---

def fetch_game_logs(person_id, person_name, season, stat_type, stat_group):
    """Fetches game logs for a specific player, season, stat type, and group."""
    hydrate_string = f"stats(group=[{stat_group}],type={stat_type},season={season}),currentTeam"

    print(f"Fetching {season} {stat_type} stats for {person_name} (ID: {person_id})...")
    # Removed hydrate string print for brevity

    try:
        api_response = statsapi.get(
            endpoint='person',
            params={'personId': person_id, 'hydrate': hydrate_string}
        )
        print(f" -> API call for {season} successful.")
        return api_response
    except Exception as e:
        print(f" -> An error occurred during the API call for {season}: {e}")
        return None

def process_response(api_response, person_id, person_name, season, stat_type, stat_group):
    """Processes the API response and extracts game logs into a DataFrame."""
    if not api_response or 'people' not in api_response or not api_response['people']:
        print(f" -> Failed to process data for {person_name} ({person_id}) in {season}: Invalid response structure.")
        # Removed pprint(api_response) for brevity
        return None

    person_info = api_response['people'][0]
    game_logs_split = None

    if 'stats' in person_info:
        for stat_entry in person_info['stats']:
            # Check if the season in the split matches the requested season
            split_season = None
            if stat_entry.get('splits') and isinstance(stat_entry['splits'], list) and len(stat_entry['splits']) > 0:
                 split_season = stat_entry['splits'][0].get('season')

            if (stat_entry.get('type', {}).get('displayName') == stat_type and
                stat_entry.get('group', {}).get('displayName') == stat_group and
                split_season == str(season)): # Ensure the split's season matches
                game_logs_split = stat_entry['splits']
                break

    if game_logs_split:
        df_season = pd.json_normalize(game_logs_split)
        # Add player identifiers to the DataFrame
        df_season['player_id'] = person_id
        df_season['player_name'] = person_name
        print(f" -> Successfully processed {len(df_season)} game logs for {season}.")
        return df_season
    else:
        print(f" -> Could not find '{stat_type}' logs for group '{stat_group}' and season {season} for {person_name} ({person_id}).")
        return None

def main():
    """Main function to fetch probable pitchers and then their game logs."""
    print("Step 1: Fetching today's probable pitchers...")
    try:
        probable_pitchers = get_probable_pitchers_today()
    except Exception as e:
        print(f"Failed to get probable pitchers: {e}")
        sys.exit(1)

    if not probable_pitchers:
        print("No probable pitchers found for today. Exiting.")
        sys.exit(0)

    print(f"\nFound {len(probable_pitchers)} probable pitchers.")
    print("Step 2: Fetching game logs for each pitcher...")

    all_pitcher_log_dfs = []

    # Ensure statsapi is usable (check kept from original)
    print("Checking if statsapi module is accessible...")
    try:
        _ = statsapi.ENDPOINTS
        print("statsapi module found.")
    except (AttributeError, ImportError):
        print("Error: Cannot find or import the 'statsapi' module or its package.")
        print("Please ensure 'mlb-statsapi' is installed (uv add mlb-statsapi)")
        sys.exit(1)

    processed_pitcher_count = 0
    for pitcher in probable_pitchers:
        player_id = pitcher.get('player_id')
        player_name = pitcher.get('name', 'Unknown Name')
        print(f"\nProcessing Pitcher: {player_name} (ID: {player_id})")

        if not player_id:
            print(" -> Skipping pitcher due to missing ID.")
            continue

        current_pitcher_season_dfs = []
        for year in SEASONS:
            response = fetch_game_logs(player_id, player_name, year, STAT_TYPE, STAT_GROUP)
            if response:
                df = process_response(response, player_id, player_name, year, STAT_TYPE, STAT_GROUP)
                if df is not None and not df.empty:
                    # Add a season column for clarity when combining (already in response? check needed)
                    # df['season_fetched_for'] = year # Example if needed
                    current_pitcher_season_dfs.append(df)
            # Add a small delay potentially if hitting API rate limits becomes an issue
            # import time; time.sleep(0.1)

        if current_pitcher_season_dfs:
            # Combine logs for the current pitcher
            pitcher_df = pd.concat(current_pitcher_season_dfs, ignore_index=True)
            all_pitcher_log_dfs.append(pitcher_df)
            processed_pitcher_count += 1
            print(f" -> Finished processing logs for {player_name}.")
        else:
            print(f" -> No game logs found for {player_name} in seasons {SEASONS}.")

        print("-" * 30) # Separator between pitchers

    if not all_pitcher_log_dfs:
        print("\nNo game log data found for any of the probable pitchers.")
        return

    print(f"\nStep 3: Combining logs from {processed_pitcher_count} pitchers...")
    final_df = pd.concat(all_pitcher_log_dfs, ignore_index=True)

    # Reorder columns to put player identifiers first
    cols = list(final_df.columns)
    id_cols = ['player_id', 'player_name']
    # Remove id_cols if they exist and insert at the beginning
    for c in reversed(id_cols):
        if c in cols:
            cols.remove(c)
            cols.insert(0, c)
    final_df = final_df[cols]


    print("\nCombined DataFrame Info:")
    final_df.info()

    print(f"\nTotal game logs fetched: {len(final_df)}")
    print("\nCombined DataFrame Head (first few rows):")
    print(final_df.head())

    # --- Save to CSV ---
    try:
        final_df.to_csv(OUTPUT_FILENAME, index=False)
        print(f"\nSuccessfully saved combined data to '{OUTPUT_FILENAME}'")
    except Exception as e:
        print(f"\nError saving data to CSV: {e}")

if __name__ == "__main__":
    main()