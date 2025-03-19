#!/usr/bin/env python3
"""
Database management module for baseball pitcher data

This module provides high-level functions for scraping and storing
baseball data, using the unified DatabaseManager.
"""

import os
import pandas as pd
from src.core.logging.config import get_logger
from src.core.db.database_manager import DatabaseManager, connect_to_database, initialize_database
from datetime import datetime

# Import the scrapers
from .gamelog_scraper import scrape_player
from .team_stats_scraper import scrape_team_stats

# Get logger for this module
logger = get_logger(__name__)

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
    
    # Create a temporary DatabaseManager for this operation
    manager = DatabaseManager()
    manager.db_path = db_path
    
    # Store data in database
    success = manager.store_pitcher_data(df, player_id, final_name)
    
    # Don't log success here since we do it in main.py
    if not success:
        logger.error(f"Failed to store data for {player_id} in database")
    
    return success

def scrape_and_store_team_stats(years=None, db_path="baseball.db"):
    """
    Scrape team stats and store in database
    
    Args:
        years (list): List of years to scrape
        db_path (str): Path to database
        
    Returns:
        bool: Success or failure
    """
    if not years:
        logger.error("No years specified")
        return False
    
    logger.info(f"Scraping team stats for years: {years}")
    
    # Create a temporary DatabaseManager for this operation
    manager = DatabaseManager()
    manager.db_path = db_path
    
    # Scrape and store each year
    success_count = 0
    for year in years:
        logger.info(f"Scraping team stats for {year}")
        
        # Scrape the team stats
        df = scrape_team_stats(year)
        
        if df is None or df.empty:
            logger.warning(f"No data found for year {year}")
            continue
        
        # Store the stats
        if manager.store_team_stats(df):
            logger.info(f"Successfully stored team stats for {year}")
            success_count += 1
        else:
            logger.error(f"Failed to store team stats for {year}")
    
    # Return true if at least one year was successful
    return success_count > 0

# Re-export the initialize_database function for backward compatibility
# This function now comes from the DatabaseManager

def get_players_in_database(db_path="baseball.db"):
    """
    Get list of players already in the database
    
    Args:
        db_path (str): Path to database
        
    Returns:
        dict: Dictionary of player_id to player_name
    """
    # Create a temporary DatabaseManager for this operation
    manager = DatabaseManager()
    manager.db_path = db_path
    
    # Get the player IDs
    return manager.get_player_ids()

def update_player_in_database(player_id, player_name, db_path="baseball.db"):
    """
    Update a player's name in the database
    
    Args:
        player_id (str): Player ID
        player_name (str): New player name
        db_path (str): Path to database
        
    Returns:
        bool: Success or failure
    """
    # Create a temporary DatabaseManager for this operation
    manager = DatabaseManager()
    manager.db_path = db_path
    
    # Update the player name
    return manager.update_player_name(player_id, player_name) 