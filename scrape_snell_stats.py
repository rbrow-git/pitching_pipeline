#!/usr/bin/env python3
"""
Scrape MLB pitcher game log data from Baseball Reference for multiple years
"""

import csv
import sys
import os
import argparse
import pandas as pd
from scrapling import StealthyFetcher
from scrapling.defaults import Fetcher

def scrape_year(player_id, year):
    """Scrape pitching data for a specific player and year"""
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=p&year={year}"
    
    print(f"Fetching data for {player_id} - {year}...")
    
    try:
        fetcher = StealthyFetcher()
        page = fetcher.fetch(
            url,
            headless=True,
            disable_resources=True,
            timeout=90000,
        )
        
        if page.status != 200:
            raise Exception(f"Failed with status code: {page.status}")
            
    except Exception as e:
        print(f"StealthyFetcher failed for {player_id} - {year}: {str(e)}")
        
        try:
            fetcher = Fetcher()
            page = fetcher.get(url, stealthy_headers=True, follow_redirects=True)
            
            if page.status != 200:
                print(f"Regular Fetcher also failed for {player_id} - {year}. Status code: {page.status}")
                return None
                
        except Exception as e2:
            print(f"All fetch attempts failed for {player_id} - {year}: {str(e2)}")
            return None
            
    print(f"Data fetched successfully for {player_id} - {year}. Extracting pitching game log...")
    
    table = page.css_first("#pitching_gamelogs")
    
    if not table:
        print(f"Could not find the pitching game log table for {player_id} - {year}")
        return None
    
    headers = []
    for th in table.css("thead th"):
        header = th.attrib.get('data-stat', '')
        if header:
            headers.append(header)
    
    rows = []
    for tr in table.css("tbody tr:not(.thead)"):
        if tr.has_class('spacer') or tr.has_class('thead'):
            continue
        
        row_data = {}
        for td in tr.css("td"):
            col_name = td.attrib.get('data-stat', '')
            if col_name in headers:
                value = td.text.clean()
                row_data[col_name] = value
        
        if row_data:
            # Add year and player_id as columns to the data
            row_data['year'] = str(year)
            row_data['player_id'] = player_id
            rows.append(row_data)
    
    if not rows:
        print(f"No data rows found in the table for {player_id} - {year}!")
        return None
        
    print(f"Found data for {len(rows)} games for {player_id} in {year}")
    
    # Convert to DataFrame
    df = pd.DataFrame(rows)
    return df

def scrape_player(player_id, years=None):
    """Scrape all available data for a specific player"""
    if years is None:
        # Default to recent years if none specified
        years = [2020, 2021, 2022, 2023, 2024]
    
    # Collect DataFrames for each year
    dfs = []
    
    for year in years:
        df = scrape_year(player_id, year)
        if df is not None and not df.empty:
            dfs.append(df)
    
    if not dfs:
        print(f"No data was successfully scraped for {player_id}.")
        return None
    
    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Combined data for {player_id}: {len(combined_df)} total games across {len(dfs)} seasons")
    
    return combined_df

def load_player_ids(csv_file):
    """Load player IDs from a CSV file"""
    try:
        df = pd.read_csv(csv_file)
        if 'Pitcher_ID' in df.columns:
            return df['Pitcher_ID'].tolist()
        else:
            print(f"Error: CSV file {csv_file} does not contain a 'Pitcher_ID' column")
            sys.exit(1)
    except Exception as e:
        print(f"Error loading player IDs from {csv_file}: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Scrape MLB pitcher game logs from Baseball Reference')
    parser.add_argument('--player-id', help='Baseball Reference player ID (e.g., snellbl01)')
    parser.add_argument('--players-file', help='CSV file containing player IDs')
    parser.add_argument('--output-dir', default='gamelogs', help='Directory to save output files')
    parser.add_argument('--years', nargs='+', type=int, help='Years to scrape (e.g., 2022 2023 2024)')
    
    args = parser.parse_args()
    
    # Set up years to scrape
    years = args.years if args.years else [2020, 2021, 2022, 2023, 2024]
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    if args.player_id:
        # Scrape a single player
        player_id = args.player_id
        df = scrape_player(player_id, years)
        
        if df is not None:
            # Save to CSV
            csv_file = os.path.join(args.output_dir, f"{player_id}_gamelogs.csv")
            try:
                df.to_csv(csv_file, index=False)
                print(f"Data saved to {csv_file}")
            except Exception as e:
                print(f"Error saving CSV file: {str(e)}")
                sys.exit(1)
                
    elif args.players_file:
        # Scrape multiple players from the CSV file
        player_ids = load_player_ids(args.players_file)
        
        # Will store combined data for all players
        all_players_df = None
        
        for player_id in player_ids:
            print(f"\nProcessing player: {player_id}")
            df = scrape_player(player_id, years)
            
            if df is not None:
                # Save individual player data
                player_csv = os.path.join(args.output_dir, f"{player_id}_gamelogs.csv")
                try:
                    df.to_csv(player_csv, index=False)
                    print(f"Data saved to {player_csv}")
                except Exception as e:
                    print(f"Error saving CSV file for {player_id}: {str(e)}")
                    continue
                
                # Append to combined dataframe
                if all_players_df is None:
                    all_players_df = df
                else:
                    all_players_df = pd.concat([all_players_df, df], ignore_index=True)
        
        # Save combined data if we have any
        if all_players_df is not None:
            combined_csv = os.path.join(args.output_dir, "all_pitchers_gamelogs.csv")
            try:
                all_players_df.to_csv(combined_csv, index=False)
                print(f"\nCombined data for all players saved to {combined_csv}")
                print(f"Total entries: {len(all_players_df)}")
            except Exception as e:
                print(f"Error saving combined CSV file: {str(e)}")
                sys.exit(1)
    
    else:
        # No player ID or file provided, show usage
        print("Please provide either a player ID or a CSV file containing player IDs.")
        print("Example usage:")
        print("  python scrape_snell_stats.py --player-id snellbl01")
        print("  python scrape_snell_stats.py --players-file starting_pitchers_ids.csv")
        print("  python scrape_snell_stats.py --player-id snellbl01 --years 2021 2022 2023")
        sys.exit(1)

if __name__ == "__main__":
    main() 