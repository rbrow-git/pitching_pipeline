#!/usr/bin/env python3
"""
Database utilities for storing baseball statistics in SQLite
This module is now a facade that imports from the modular db package
"""

# Import all the functions from the new modular structure
from src.core.db.schema import create_database
from src.core.db.pitcher_utils import (
    store_pitcher_data, 
    get_stored_pitcher_data, 
    get_all_pitcher_data, 
    update_player_name, 
    get_stored_player_ids
)
from src.core.db.team_utils import store_team_stats, get_team_stats, get_team_ids

# Re-export everything for backward compatibility
__all__ = [
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