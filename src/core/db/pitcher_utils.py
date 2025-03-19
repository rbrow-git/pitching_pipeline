#!/usr/bin/env python3
"""
Utilities for storing and retrieving pitcher data
"""

import sqlite3
import pandas as pd
from datetime import datetime
from .column_mapping import pitcher_column_mapping
from src.core.logging.config import get_logger

logger = get_logger(__name__)

def store_pitcher_data(df, player_id, db_path="baseball.db", player_name=None):
    """
    Store pitcher data into SQLite database
    
    Args:
        df (DataFrame): DataFrame containing pitcher game logs
        player_id (str): Player ID
        db_path (str): Path to database
        player_name (str): Player name
        
    Returns:
        bool: Success or failure
    """
    if df is None or df.empty:
        logger.warning(f"No data to store for {player_id}")
        return False
    
    conn = None  # Initialize conn to None to avoid UnboundLocalError
    
    try:
        # Make a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Add player_id column if not present
        if 'player_id' not in df_copy.columns:
            df_copy['player_id'] = player_id
        
        # Apply column mapping - rename columns to match database schema
        df_copy = df_copy.rename(columns={k: v for k, v in pitcher_column_mapping.items() if k in df_copy.columns})
        
        # Convert numeric columns to appropriate types
        for col in df_copy.columns:
            if col in ['innings_pitched', 'era', 'whip', 'win_probability_added', 'average_leverage_index', 'run_expectancy_24']:
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
            elif col not in ['player_id', 'date_game', 'team_id', 'opponent_id', 'game_result']:
                # Use pandas nullable integer type for safe conversion
                df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
                # Use Int64 for columns that were successfully converted to numeric, otherwise leave as object
                if not df_copy[col].isna().all():  # Only if column has some non-NA values
                    try:
                        df_copy[col] = df_copy[col].astype('Int64')
                    except (ValueError, TypeError):
                        logger.warning(f"Could not convert column {col} to Int64, leaving as float")
        
        # Handle missing dates - filter out rows with missing date values instead of setting defaults
        if 'date_game' in df_copy.columns:
            # Print date values for debugging
            logger.debug(f"Date values for {player_id} before filtering: {df_copy['date_game'].tolist()[:5]}...")
            
            # Create a mask for missing dates
            missing_dates = df_copy['date_game'].isna() | (df_copy['date_game'] == '') | (df_copy['date_game'].str.lower() == 'none')
            
            # Count missing dates
            num_missing = missing_dates.sum()
            if num_missing > 0:
                logger.warning(f"Filtering out {num_missing} rows with missing date values for {player_id}")
                
                # Filter out rows with missing dates
                df_copy = df_copy[~missing_dates]
                
            # Print date values for debugging
            logger.debug(f"Date values for {player_id} after filtering: {df_copy['date_game'].tolist()[:5]}...")
        
        # Handle road_indicator (convert non-null values to 1)
        if 'road_indicator' in df_copy.columns:
            logger.debug(f"Road indicator values before conversion: {df_copy['road_indicator'].tolist()[:5]}...")
            # Convert non-null values to 1 (indicating road game)
            df_copy['road_indicator'] = df_copy['road_indicator'].apply(
                lambda x: 1 if pd.notna(x) and x == '@' else 0
            )
            logger.debug(f"Road indicator values after conversion: {df_copy['road_indicator'].tolist()[:5]}...")
        
        # Filter out summary/header rows (where team_id is "Tm" or opponent_id is "Opp")
        if 'team_id' in df_copy.columns and 'opponent_id' in df_copy.columns:
            original_len = len(df_copy)
            df_copy = df_copy[~((df_copy['team_id'] == 'Tm') | (df_copy['opponent_id'] == 'Opp'))]
            filtered_len = len(df_copy)
            if original_len > filtered_len:
                logger.info(f"Filtered out {original_len - filtered_len} summary/header rows for {player_id}")
        
        # Get only the columns that match the database schema
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the column names of the table
        cursor.execute("PRAGMA table_info(pitching_gamelogs)")
        db_columns = [row[1] for row in cursor.fetchall() if row[1] != 'id']  # exclude id column
        
        # Filter the DataFrame to keep only the columns that match the database schema
        available_columns = [col for col in df_copy.columns if col in db_columns]
        
        # Log schema mismatch information if in verbose mode
        missing_columns = set(db_columns) - set(available_columns)
        extra_columns = set(df_copy.columns) - set(db_columns)
        if missing_columns:
            logger.debug(f"Missing columns in data: {', '.join(missing_columns)}")
        if extra_columns:
            logger.debug(f"Extra columns in data not in schema: {', '.join(extra_columns)}")
        
        df_filtered = df_copy[available_columns]
        
        # Drop duplicates based on player_id, date_game, and year to avoid removing games from different years
        if 'player_id' in df_filtered.columns and 'date_game' in df_filtered.columns:
            # If we have a year column, include it in the duplicate detection
            if 'year' in df_filtered.columns:
                old_len = len(df_filtered)
                df_filtered = df_filtered.drop_duplicates(subset=['player_id', 'date_game', 'year'])
                new_len = len(df_filtered)
                if old_len > new_len:
                    logger.info(f"Dropped {old_len - new_len} duplicate rows for {player_id} (using player_id, date_game, and year)")
            else:
                # Fall back to just player_id and date_game if year is not available
                old_len = len(df_filtered)
                df_filtered = df_filtered.drop_duplicates(subset=['player_id', 'date_game'])
                new_len = len(df_filtered)
                if old_len > new_len:
                    logger.info(f"Dropped {old_len - new_len} duplicate rows for {player_id} (using player_id and date_game only)")
        
        # Print dtypes for debugging
        logger.debug(f"DataFrame column dtypes before SQL insert: {df_filtered.dtypes}")
        
        # First, delete any existing records with the same player_id
        try:
            cursor.execute("DELETE FROM pitching_gamelogs WHERE player_id = ?", (player_id,))
            deleted_count = cursor.rowcount
            logger.info(f"Deleted {deleted_count} existing records for {player_id}")
            
            # We need to commit the DELETE before inserting to avoid constraint errors
            conn.commit()
        except Exception as del_e:
            logger.error(f"Error deleting existing records for {player_id}: {str(del_e)}")
            conn.rollback()
            # Don't return here, continue with INSERT operation
        
        # Now insert data into database
        try:
            df_filtered.to_sql('pitching_gamelogs', conn, if_exists='append', index=False)
            logger.info(f"Successfully inserted {len(df_filtered)} rows for {player_id}")
        except Exception as ins_e:
            logger.error(f"Error inserting records for {player_id}: {str(ins_e)}")
            conn.rollback()
            return False
        
        # Update player information
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
        INSERT OR REPLACE INTO players (player_id, player_name, last_updated)
        VALUES (?, ?, ?)
        """, (player_id, player_name, timestamp))
        
        conn.commit()
        rows_affected = len(df_filtered)
        logger.info(f"Stored {rows_affected} rows for {player_id} in database")
        return True
    
    except Exception as e:
        logger.error(f"Error storing data for {player_id}: {str(e)}")
        if conn:
            try:
                conn.rollback()  # Rollback transaction on error
            except:
                pass
        return False
    
    finally:
        if conn:
            conn.close()


def update_player_name(player_id, player_name, db_path="baseball.db"):
    """
    Update a player's name in the database
    
    Args:
        player_id (str): Player ID
        player_name (str): New player name
        db_path (str): Path to database
        
    Returns:
        bool: Success or failure
    """
    if not player_id or not player_name:
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if player exists
        cursor.execute("SELECT player_id FROM players WHERE player_id = ?", (player_id,))
        if not cursor.fetchone():
            logger.warning(f"Player {player_id} does not exist in database")
            return False
        
        # Update player name
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
        UPDATE players 
        SET player_name = ?, last_updated = ?
        WHERE player_id = ?
        """, (player_name, timestamp, player_id))
        
        conn.commit()
        logger.debug(f"Updated name for {player_id} to '{player_name}'")
        return True
    
    except Exception as e:
        logger.error(f"Error updating player name for {player_id}: {str(e)}")
        return False
    
    finally:
        if conn:
            conn.close()


def get_stored_pitcher_data(player_id, db_path="baseball.db"):
    """
    Retrieve pitcher data from the database
    
    Args:
        player_id (str): Player ID
        db_path (str): Path to database
        
    Returns:
        DataFrame: DataFrame with pitcher data
    """
    try:
        conn = sqlite3.connect(db_path)
        query = f"SELECT * FROM pitching_gamelogs WHERE player_id = ?"
        df = pd.read_sql_query(query, conn, params=(player_id,))
        return df
    
    except Exception as e:
        logger.error(f"Error retrieving data for {player_id}: {str(e)}")
        return None
    
    finally:
        if conn:
            conn.close()


def get_all_pitcher_data(db_path="baseball.db"):
    """
    Retrieve all pitcher data from the database
    
    Args:
        db_path (str): Path to database
        
    Returns:
        DataFrame: DataFrame with all pitcher data
    """
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM pitching_gamelogs"
        df = pd.read_sql_query(query, conn)
        return df
    
    except Exception as e:
        logger.error(f"Error retrieving all pitcher data: {str(e)}")
        return None
    
    finally:
        if conn:
            conn.close()


def get_stored_player_ids(db_path="baseball.db"):
    """
    Get list of player IDs already in the database
    
    Args:
        db_path (str): Path to database
        
    Returns:
        dict: Dictionary mapping player_id to player_name
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT player_id, player_name FROM players")
        players = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return players
    except:
        return {} 