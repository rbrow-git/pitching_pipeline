#!/usr/bin/env python3
"""
Unified Database Manager for Baseball Pitching Pipeline

This module provides a single interface for all database operations,
consolidating the functionality that was previously spread across
multiple modules.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from src.core.logging.config import get_logger
from .schema import create_database
from .pitcher_utils import store_pitcher_data, get_stored_pitcher_data, get_all_pitcher_data, update_player_name, get_stored_player_ids
from .team_utils import store_team_stats, get_team_stats, get_team_ids

# Get logger for this module
logger = get_logger(__name__)

class DatabaseManager:
    """
    Database Manager class for unified access to all database operations
    
    This class provides a single interface for all database operations,
    including creating the database, storing and retrieving pitcher data,
    and storing and retrieving team statistics.
    """
    
    def __init__(self, db_path="baseball.db"):
        """
        Initialize the DatabaseManager with a database path
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
    
    def initialize_database(self, force_recreate=False):
        """
        Initialize the database and create tables if they don't exist
        
        Args:
            force_recreate (bool): Whether to drop and recreate existing tables
            
        Returns:
            str: Path to the initialized database
        """
        self.db_path = create_database(self.db_path, force_recreate=force_recreate)
        logger.info(f"Using database at {self.db_path}")
        return self.db_path
    
    def store_pitcher_data(self, df, player_id, player_name=None):
        """
        Store pitcher data in the database
        
        Args:
            df (DataFrame): DataFrame containing pitcher game logs
            player_id (str): Player ID
            player_name (str): Player name
            
        Returns:
            bool: Success or failure
        """
        return store_pitcher_data(df, player_id, self.db_path, player_name)
    
    def get_pitcher_data(self, player_id):
        """
        Retrieve pitcher data from the database
        
        Args:
            player_id (str): Player ID
            
        Returns:
            DataFrame: DataFrame with pitcher data
        """
        return get_stored_pitcher_data(player_id, self.db_path)
    
    def get_all_pitchers(self):
        """
        Retrieve all pitcher data from the database
        
        Returns:
            DataFrame: DataFrame with all pitcher data
        """
        return get_all_pitcher_data(self.db_path)
    
    def get_player_ids(self):
        """
        Get list of player IDs already in the database
        
        Returns:
            dict: Dictionary mapping player_id to player_name
        """
        return get_stored_player_ids(self.db_path)
    
    def update_player_name(self, player_id, player_name):
        """
        Update a player's name in the database
        
        Args:
            player_id (str): Player ID
            player_name (str): New player name
            
        Returns:
            bool: Success or failure
        """
        return update_player_name(player_id, player_name, self.db_path)
    
    def store_team_stats(self, df):
        """
        Store team stats in the database
        
        Args:
            df (DataFrame): Team stats dataframe
            
        Returns:
            bool: Success or failure
        """
        return store_team_stats(df, self.db_path)
    
    def get_team_stats(self, team_id=None, year=None):
        """
        Retrieve team stats from the database
        
        Args:
            team_id (str): Team ID to filter by, or None for all teams
            year (int): Year to filter by, or None for all years
            
        Returns:
            DataFrame: DataFrame with team statistics
        """
        return get_team_stats(team_id, year, self.db_path)
    
    def get_team_ids(self):
        """
        Get list of team IDs in the database
        
        Returns:
            list: List of unique team IDs
        """
        return get_team_ids(self.db_path)

# Create a singleton instance for easy import
db_manager = DatabaseManager()

# Functions to maintain backwards compatibility
def initialize_database(db_path="baseball.db", force_recreate=False):
    """
    Initialize the database and return its path - convenience function
    
    Args:
        db_path (str): Path to database
        force_recreate (bool): Whether to recreate the database if it exists
        
    Returns:
        str: Path to database
    """
    # Use a temporary DatabaseManager instance with the specified path
    manager = DatabaseManager(db_path)
    return manager.initialize_database(force_recreate=force_recreate)

def connect_to_database(db_path="baseball.db"):
    """
    Connect to the database and return a connection
    
    Args:
        db_path (str): Path to database
        
    Returns:
        Connection: SQLite database connection
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None 