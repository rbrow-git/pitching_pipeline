#!/usr/bin/env python3
"""
Main script for scraping pitcher data and storing in SQLite database
"""

import argparse
import os
import sys
import logging
import pandas as pd
from datetime import datetime

from scraper import scrape_player
from db_utils import create_database, store_pitcher_data, get_stored_player_ids, update_player_name

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_player_ids(filepath):
    """
    Load player IDs from a CSV file
    
    The CSV file should have a simple format with one column named 'player_id'
    containing Baseball Reference player IDs.
    
    Example CSV format:
    player_id
    snellbl01
    scheram01
    degroja01
    """
    try:
        df = pd.read_csv(filepath)
        
        # Check for required column
        if 'player_id' not in df.columns:
            logger.error(f"Error: CSV file {filepath} doesn't have a 'player_id' column")
            return []
        
        # Get unique player IDs as a list
        player_ids = df['player_id'].unique().tolist()
        return player_ids
        
    except Exception as e:
        logger.error(f"Error loading player IDs from {filepath}: {str(e)}")
        return []


def scrape_and_store(player_id, years=None, db_path="baseball.db", player_name=None):
    """Scrape player data and store in database"""
    # Check if we already have this player's data for these years
    logger.info(f"Scraping data for {player_id}{' (' + player_name + ')' if player_name else ''} for years {years}")
    
    # Scrape the player data
    df, extracted_name = scrape_player(player_id, years)
    
    if df is None or df.empty:
        logger.warning(f"No data found for {player_id}")
        return False
    
    # Use provided name if available, otherwise use extracted name
    final_name = player_name if player_name else extracted_name
    if extracted_name and not player_name:
        logger.info(f"Using extracted player name: {extracted_name}")
    
    # Store data in database
    success = store_pitcher_data(df, player_id, db_path, final_name)
    if success:
        logger.info(f"Successfully stored data for {player_id} in database")
    else:
        logger.error(f"Failed to store data for {player_id} in database")
    
    return success


def main():
    """Main function for scraping pitcher data"""
    parser = argparse.ArgumentParser(description="Scrape MLB pitcher game logs from Baseball Reference")
    
    # Arguments for specifying what to scrape
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--player-id', type=str, help="Baseball Reference player ID to scrape")
    input_group.add_argument('--players-file', type=str, help="CSV file containing player_id column")
    
    # Optional arguments
    parser.add_argument('--player-name', type=str, help="Player name (only used with --player-id)")
    parser.add_argument('--years', type=int, nargs='+', help="Years to scrape (default: 2021-2024)")
    parser.add_argument('--db-path', type=str, default="baseball.db", help="Path to SQLite database")
    parser.add_argument('--skip-existing', action='store_true', help="Skip players already in database")
    parser.add_argument('--limit', type=int, help="Limit number of players to scrape")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose logging")
    parser.add_argument('--reset-db', action='store_true', help="Force recreate the database tables")
    parser.add_argument('--update-names', action='store_true', help="Update player names in database without scraping")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create database if it doesn't exist
    db_path = create_database(args.db_path, force_recreate=args.reset_db)
    logger.info(f"Using database at {db_path}")
    
    # Get stored player IDs if needed
    stored_players = {}
    if args.skip_existing or args.update_names:
        stored_players = get_stored_player_ids(db_path)
        logger.info(f"Found {len(stored_players)} players already in database")
    
    # Determine which years to scrape
    years = args.years if args.years else list(range(2021, 2025))  # Default to 2021-2024
    
    # Handle single player
    if args.player_id:
        player_id = args.player_id
        player_name = args.player_name
        
        if args.update_names and player_name:
            # Just update the player name
            if update_player_name(player_id, player_name, db_path):
                logger.info(f"Updated name for {player_id} to '{player_name}'")
            else:
                logger.error(f"Failed to update name for {player_id}")
            return
            
        if player_id in stored_players and args.skip_existing:
            logger.info(f"Skipping {player_id} (already in database)")
        else:
            scrape_and_store(player_id, years, db_path, player_name)
    
    # Handle multiple players from file
    elif args.players_file:
        player_ids = load_player_ids(args.players_file)
        
        if not player_ids:
            logger.error("No valid player IDs found in file")
            return
        
        logger.info(f"Loaded {len(player_ids)} player IDs from {args.players_file}")
        
        # Apply limit if specified
        if args.limit and args.limit > 0:
            player_ids = player_ids[:args.limit]
            logger.info(f"Limited to first {args.limit} players")
        
        # Scrape each player
        success_count = 0
        for i, player_id in enumerate(player_ids):
            logger.info(f"Processing {i+1}/{len(player_ids)}: {player_id}")
            
            if player_id in stored_players and args.skip_existing:
                logger.info(f"Skipping {player_id} (already in database)")
                continue
            
            if scrape_and_store(player_id, years, db_path):
                success_count += 1
        
        logger.info(f"Completed scraping {success_count}/{len(player_ids)} players")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        sys.exit(1) 