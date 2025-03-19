#!/usr/bin/env python3
"""
Script for scraping baseball pitcher game logs and storing them in the database
"""

import argparse
import sys
import logging
import os
from datetime import datetime

# Core imports
from src.core.db_manager import scrape_and_store, initialize_database
from src.core.player_utils import load_player_ids, filter_players

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Scrape pitcher game logs and store them in the database"""
    parser = argparse.ArgumentParser(description="Scrape MLB pitcher game logs and store in database")
    
    # Input file options
    parser.add_argument('--test', action='store_true',
                      help="Use test_ids.csv instead of starting_pitchers_ids.csv")
    parser.add_argument('--input-file', type=str,
                      help="Custom CSV file containing player_id column (overrides --test)")
    
    # Database and scraping options
    parser.add_argument('--years', type=int, nargs='+', 
                      help="Years to scrape (default: 2021-current)")
    parser.add_argument('--db-path', type=str, default="baseball.db",
                      help="Path to SQLite database")
    parser.add_argument('--limit', type=int, 
                      help="Limit number of players to scrape")
    parser.add_argument('--reset-db', action='store_true',
                      help="Force recreate the database tables")
    parser.add_argument('--verbose', '-v', action='store_true',
                      help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Determine which input file to use
    if args.input_file:
        players_file = args.input_file
        logger.info(f"Using custom input file: {players_file}")
    elif args.test:
        # Use test_ids.csv from csv directory
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        players_file = os.path.join(script_dir, "csv", "test_ids.csv")
        logger.info(f"Using test input file: {players_file}")
    else:
        # Use starting_pitchers_ids.csv from csv directory
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        players_file = os.path.join(script_dir, "csv", "starting_pitchers_ids.csv")
        logger.info(f"Using main input file: {players_file}")
    
    # Initialize database (always create or reset)
    db_path = initialize_database(args.db_path, force_recreate=args.reset_db)
    
    # Determine which years to scrape
    years = args.years if args.years else list(range(2021, datetime.now().year + 1))
    logger.info(f"Scraping years: {years}")
    
    # Load player IDs from file
    player_ids = load_player_ids(players_file)
    if not player_ids:
        logger.error(f"No valid player IDs found in file: {players_file}")
        return
    
    logger.info(f"Loaded {len(player_ids)} player IDs from {players_file}")
    
    # Apply limit if specified
    if args.limit and args.limit > 0:
        player_ids = filter_players(player_ids, limit=args.limit)
    
    logger.info(f"Will scrape {len(player_ids)} players")
    
    # Scrape each player
    success_count = 0
    for i, player_id in enumerate(player_ids):
        logger.info(f"Processing {i+1}/{len(player_ids)}: {player_id}")
        
        if scrape_and_store(player_id, years, db_path):
            success_count += 1
    
    logger.info(f"Completed scraping {success_count}/{len(player_ids)} players")
    logger.info(f"Game logs saved to database at {db_path}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        sys.exit(1) 