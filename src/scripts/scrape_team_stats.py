#!/usr/bin/env python3
"""
Script for scraping MLB team batting statistics and storing them in the database
"""

import argparse
import sys
import logging
from datetime import datetime

from src.core.db_manager import scrape_and_store_team_stats, initialize_database

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Scrape team batting statistics and store in database"""
    parser = argparse.ArgumentParser(description="Scrape MLB team batting statistics")
    
    # Years to scrape
    parser.add_argument('--years', type=int, nargs='+', 
                      help="Years to scrape (default: current year)")
    
    # Database options
    parser.add_argument('--db-path', type=str, default="baseball.db",
                      help="Path to SQLite database")
    parser.add_argument('--reset-db', action='store_true',
                      help="Force recreate the database tables")
    
    # Other options
    parser.add_argument('--verbose', '-v', action='store_true',
                      help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize database
    db_path = initialize_database(args.db_path, force_recreate=args.reset_db)
    
    # Determine which years to scrape
    years = args.years
    if not years:
        years = [datetime.now().year]
    
    logger.info(f"Scraping team stats for years: {years}")
    
    # Scrape and store team stats
    success = scrape_and_store_team_stats(years, db_path)
    
    if success:
        logger.info("✅ Team stats scraping completed successfully")
    else:
        logger.error("❌ Team stats scraping failed")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        sys.exit(1) 