"""
Database utilities for storing and retrieving baseball statistics

This package provides both low-level database functions and a high-level
DatabaseManager class for unified database access.
"""

# Import the low-level functions for backward compatibility
from .schema import create_database
from .pitcher_utils import store_pitcher_data, get_stored_pitcher_data, get_all_pitcher_data, update_player_name, get_stored_player_ids
from .team_utils import store_team_stats, get_team_stats, get_team_ids

# Import the new DatabaseManager class and singleton instance
from .database_manager import DatabaseManager, db_manager, initialize_database

# Export everything for use
__all__ = [
    # Classes
    'DatabaseManager',
    
    # Singleton instances
    'db_manager',
    
    # Functions
    'initialize_database',
    'create_database',
    'store_pitcher_data',
    'get_stored_pitcher_data',
    'get_all_pitcher_data',
    'update_player_name',
    'get_stored_player_ids',
    'store_team_stats',
    'get_team_stats',
    'get_team_ids'
] 