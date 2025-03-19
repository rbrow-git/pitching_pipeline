#!/usr/bin/env python3
"""
Main CLI for Baseball Pitching Pipeline.

Provides commands for scraping pitcher game logs and team stats,
as well as for managing database interactions.
"""

import argparse
import sys
import os
from datetime import datetime

# Add the parent directory to sys.path so that 'src' imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the core functionality
from src.core.scraper_manager import scrape_and_store, scrape_and_store_team_stats, initialize_database
from src.core.player_utils import load_player_ids, filter_players
from src.core.logging.config import setup_logging, get_logger

# Setup logging early with default settings (will be configured properly in main)
setup_logging(False)

# Initialize logger
logger = get_logger(__name__)

def handle_pitchers(args):
    """Handle the 'pitchers' subcommand to scrape pitcher game logs"""
    # Determine which input file to use
    if args.input_file:
        players_file = args.input_file
        logger.info(f"Using custom input file: {players_file}")
    elif args.test:
        players_file = "src/data/test_ids.csv"
        logger.info(f"Using test input file: {players_file}")
    else:
        players_file = "src/data/starting_pitchers_ids.csv"
        logger.info(f"Using default input file: {players_file}")
    
    # Determine database path and create if needed
    db_path = initialize_database(args.db_path, force_recreate=args.reset_db)
    logger.info(f"[ESSENTIAL] Using database at {db_path}")
    
    # Determine years to scrape
    if args.years:
        years = args.years
    else:
        current_year = datetime.now().year
        years = list(range(2021, current_year + 1))
    logger.info(f"Scraping years: {years}")
    
    # Load player IDs
    player_ids = load_player_ids(players_file)
    logger.info(f"Loaded {len(player_ids)} player IDs from {players_file}")
    
    # Apply limit if specified
    if args.limit and args.limit < len(player_ids):
        original_count = len(player_ids)
        player_ids = player_ids[:args.limit]
        logger.info(f"Limited to first {args.limit} players")
    
    logger.info(f"[ESSENTIAL] Will scrape {len(player_ids)} players")
    
    # Track success count
    success_count = 0
    
    # Process each player
    for i, player_id in enumerate(player_ids, 1):
        logger.info(f"[ESSENTIAL] Processing {i}/{len(player_ids)}: {player_id}")
        logger.debug(f"Scraping data for {player_id} for years {years}")
        
        # Scrape and store
        if scrape_and_store(player_id, years, db_path):
            logger.info(f"[ESSENTIAL] Successfully stored data for {player_id} in database")
            success_count += 1
        else:
            logger.error(f"Failed to store data for {player_id} in database")
    
    logger.info(f"[ESSENTIAL] Completed scraping {success_count}/{len(player_ids)} players")
    logger.info(f"Game logs saved to database at {db_path}")
    
    return 0 if success_count > 0 else 1

def handle_teams(args):
    """Handle the 'teams' subcommand to scrape team batting stats"""
    # Initialize database
    db_path = initialize_database(args.db_path, force_recreate=args.reset_db)
    
    # Determine which years to scrape
    years = args.years
    if not years:
        years = [datetime.now().year]
    
    logger.info(f"[ESSENTIAL] Scraping team stats for years: {years}")
    
    # Scrape and store team stats
    success = scrape_and_store_team_stats(years, db_path)
    
    if success:
        logger.info("[ESSENTIAL] ✅ Team stats scraping completed successfully")
        return 0
    else:
        logger.error("❌ Team stats scraping failed")
        return 1

def get_environment_verbose():
    """Check environment variable for verbose mode setting"""
    env_verbose = os.environ.get("BASEBALL_VERBOSE", "").lower()
    return env_verbose in ("1", "true", "yes", "on")

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Baseball Pitching Pipeline CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True
    
    # Subcommand for scraping pitcher game logs
    parser_pitchers = subparsers.add_parser("pitchers", help="Scrape pitcher game logs")
    parser_pitchers.add_argument("--test", action="store_true",
                      help="Use test_ids.csv instead of starting_pitchers_ids.csv")
    parser_pitchers.add_argument("--input-file", type=str,
                      help="Custom CSV file containing player_id column (overrides --test)")
    parser_pitchers.add_argument("--years", type=int, nargs="+", 
                      help="Years to scrape (default: 2021-current)")
    parser_pitchers.add_argument("--db-path", type=str, default="baseball.db",
                      help="Path to SQLite database")
    parser_pitchers.add_argument("--limit", type=int, 
                      help="Limit number of players to scrape")
    parser_pitchers.add_argument("--reset-db", action="store_true",
                      help="Force recreate the database tables")
    parser_pitchers.add_argument("--verbose", "-v", action="store_true",
                      help="Enable verbose logging")
    parser_pitchers.set_defaults(func=handle_pitchers)
    
    # Subcommand for scraping team stats
    parser_teams = subparsers.add_parser("teams", help="Scrape team batting stats")
    parser_teams.add_argument("--years", type=int, nargs="+", 
                      help="Years to scrape (default: current year)")
    parser_teams.add_argument("--db-path", type=str, default="baseball.db",
                      help="Path to SQLite database")
    parser_teams.add_argument("--reset-db", action="store_true",
                      help="Force recreate the database tables")
    parser_teams.add_argument("--verbose", "-v", action="store_true",
                      help="Enable verbose logging")
    parser_teams.set_defaults(func=handle_teams)
    
    args = parser.parse_args()
    
    # Set up logging with verbosity setting
    # Check command line args first, then environment variable
    verbose = False
    if hasattr(args, "verbose") and args.verbose:
        verbose = True
    elif get_environment_verbose():
        verbose = True
        
    # Configure logging
    setup_logging(verbose)
    
    if verbose:
        logger.debug("Verbose logging enabled")
    
    # Call the appropriate function based on the subcommand
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        sys.exit(1) 