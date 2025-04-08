import statsapi
import datetime
import traceback

def get_probable_pitchers_today():
    """
    Fetches probable pitchers for today's MLB games using the statsapi.
    Finds pitcher names from the schedule, then looks up their IDs.
    Returns a list of dictionaries, each containing pitcher details.
    """
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    print(f"Fetching schedule for today: {today_str}")
    pitchers_list = []

    try:
        schedule = statsapi.schedule(date=today_str)

        if not schedule:
            print("No games scheduled for today or failed to fetch schedule.")
            return []

        print(f"Found {len(schedule)} games scheduled for today.")

        for i, game in enumerate(schedule):
            game_pk = game.get('game_id')
            away_team = game.get('away_name', 'Unknown Away Team')
            home_team = game.get('home_name', 'Unknown Home Team')
            # Get names only first
            away_probable_pitcher_name = game.get('away_probable_pitcher', 'TBD')
            home_probable_pitcher_name = game.get('home_probable_pitcher', 'TBD')

            # --- Process Away Pitcher --- 
            if away_probable_pitcher_name and away_probable_pitcher_name != 'TBD':
                print(f"Game {i+1} ({away_team} @ {home_team}): Found away pitcher name '{away_probable_pitcher_name}'. Looking up ID...")
                try:
                    player_lookup = statsapi.lookup_player(away_probable_pitcher_name)
                    if player_lookup:
                        away_pitcher_id = player_lookup[0].get('id')
                        if away_pitcher_id:
                            print(f" -> Found ID: {away_pitcher_id}")
                            pitchers_list.append({
                                'name': away_probable_pitcher_name,
                                'player_id': away_pitcher_id,
                                'opponent_today': home_team,
                                'at_home_today': 0,
                                'game_pk_today': game_pk
                            })
                        else:
                            print(f" -> ID lookup successful but no 'id' key found for {away_probable_pitcher_name}.")
                    else:
                        print(f" -> Player ID lookup failed for {away_probable_pitcher_name} (no results).")
                except Exception as e:
                    print(f" -> Error during player ID lookup for {away_probable_pitcher_name}: {e}")
            # No need for the elif check from before

            # --- Process Home Pitcher --- 
            if home_probable_pitcher_name and home_probable_pitcher_name != 'TBD':
                print(f"Game {i+1} ({away_team} @ {home_team}): Found home pitcher name '{home_probable_pitcher_name}'. Looking up ID...")
                try:
                    player_lookup = statsapi.lookup_player(home_probable_pitcher_name)
                    if player_lookup:
                        home_pitcher_id = player_lookup[0].get('id')
                        if home_pitcher_id:
                            print(f" -> Found ID: {home_pitcher_id}")
                            pitchers_list.append({
                                'name': home_probable_pitcher_name,
                                'player_id': home_pitcher_id,
                                'opponent_today': away_team,
                                'at_home_today': 1,
                                'game_pk_today': game_pk
                            })
                        else:
                            print(f" -> ID lookup successful but no 'id' key found for {home_probable_pitcher_name}.")
                    else:
                        print(f" -> Player ID lookup failed for {home_probable_pitcher_name} (no results).")
                except Exception as e:
                    print(f" -> Error during player ID lookup for {home_probable_pitcher_name}: {e}")
            # No need for the elif check from before

        print(f"\nFinished processing games. Successfully extracted {len(pitchers_list)} probable pitcher entries with IDs.")
        return pitchers_list

    except ImportError:
        print("Error: The 'mlb-statsapi' package is not installed.")
        print("Please install it using: uv add mlb-statsapi")
        raise
    except Exception as e:
        print(f"An error occurred while fetching schedule or looking up players: {e}")
        print(traceback.format_exc())
        return []

# Module only - no main execution block needed here 