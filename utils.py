#!/usr/bin/env python3
"""
Utility functions for baseball data scraping
"""

import os
import sys
import pandas as pd


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


def filter_players_to_scrape(all_players, stored_players, max_players=None):
    """
    Filter the list of players to scrape, prioritizing new players
    
    Args:
        all_players: List of all player IDs
        stored_players: List of player IDs already in the database
        max_players: Maximum number of players to process (None for all)
        
    Returns:
        List of player IDs to scrape
    """
    # Find players not yet in the database
    new_players = [p for p in all_players if p not in stored_players]
    
    # If max_players is specified, limit the number of players
    if max_players is not None:
        # Prioritize new players, then add existing ones if needed
        if len(new_players) >= max_players:
            return new_players[:max_players]
        else:
            # Add some existing players to reach max_players
            existing_to_add = max_players - len(new_players)
            return new_players + stored_players[:existing_to_add]
    else:
        # Process all players, new ones first
        return new_players + stored_players


def get_valid_years(min_year=1900, max_year=2024):
    """
    Get a list of valid years for scraping
    
    Args:
        min_year: Minimum year to include
        max_year: Maximum year to include (defaults to current year)
        
    Returns:
        List of valid years
    """
    import datetime
    
    # If max_year is None, use current year
    if max_year is None:
        max_year = datetime.datetime.now().year
        
    return list(range(min_year, max_year + 1)) 