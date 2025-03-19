#!/usr/bin/env python3
"""
Utilities for working with player data
"""

import logging
import pandas as pd

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

def filter_players(player_ids, limit=None, stored_players=None, skip_existing=False):
    """
    Filter the list of player IDs based on various criteria
    
    Args:
        player_ids: List of player IDs to filter
        limit: Maximum number of players to return
        stored_players: Dictionary of players already in the database
        skip_existing: Whether to skip players already in the database
        
    Returns:
        Filtered list of player IDs
    """
    if not player_ids:
        return []
    
    # Skip existing players if requested
    if skip_existing and stored_players:
        player_ids = [pid for pid in player_ids if pid not in stored_players]
        logger.info(f"Filtered out existing players, {len(player_ids)} remaining")
    
    # Apply limit if specified
    if limit and limit > 0 and len(player_ids) > limit:
        player_ids = player_ids[:limit]
        logger.info(f"Limited to first {limit} players")
    
    return player_ids 