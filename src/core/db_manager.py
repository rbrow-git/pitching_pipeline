#!/usr/bin/env python3
"""
Database management module for baseball pitcher data
"""

import logging
import pandas as pd

# Use the already refactored db_utils as the facade to maintain compatibility
from .db_utils import (
    create_database, 
    store_pitcher_data, 
    store_team_stats
)
from .gamelog_scraper import scrape_player
from .team_stats_scraper import scrape_team_stats

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_and_store(player_id, years=None, db_path="baseball.db", player_name=None):
    """
    Scrape player data and store in database
    
    Args:
        player_id (str): Player ID to scrape
        years (list): List of years to scrape
        db_path (str): Path to database
        player_name (str): Optional player name override
        
    Returns:
        bool: Success or failure
    """
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

def scrape_and_store_team_stats(years=None, db_path="baseball.db"):
    """
    Scrape team batting statistics and store in database
    
    Args:
        years (list): List of years to scrape, defaults to current year only
        db_path (str): Path to database
        
    Returns:
        bool: Success or failure
    """
    # Use single current year if not specified
    if not years:
        from datetime import datetime
        years = [datetime.now().year]
    
    logger.info(f"Scraping team stats for years: {years}")
    
    success_count = 0
    for year in years:
        logger.info(f"Scraping team stats for {year}")
        
        # Scrape team stats for this year
        df = scrape_team_stats(year)
        
        if df is None or df.empty:
            logger.warning(f"No team stats found for {year}")
            continue
        
        # Store in database
        success = store_team_stats(df, db_path)
        if success:
            logger.info(f"Successfully stored team stats for {year} in database")
            success_count += 1
        else:
            logger.error(f"Failed to store team stats for {year} in database")
    
    logger.info(f"Completed scraping team stats for {success_count}/{len(years)} years")
    return success_count > 0

def initialize_database(db_path="baseball.db", force_recreate=False):
    """
    Initialize the database and return its path
    
    Args:
        db_path (str): Path to database
        force_recreate (bool): Whether to recreate the database if it exists
        
    Returns:
        str: Path to database
    """
    db_path = create_database(db_path, force_recreate=force_recreate)
    logger.info(f"Using database at {db_path}")
    return db_path

def get_players_in_database(db_path="baseball.db"):
    """Get a dictionary of players already in the database"""
    stored_players = get_stored_player_ids(db_path)
    logger.info(f"Found {len(stored_players)} players already in database")
    return stored_players

def update_player_in_database(player_id, player_name, db_path="baseball.db"):
    """Update a player's name in the database"""
    if update_player_name(player_id, player_name, db_path):
        logger.info(f"Updated name for {player_id} to '{player_name}'")
        return True
    else:
        logger.error(f"Failed to update name for {player_id}")
        return False 