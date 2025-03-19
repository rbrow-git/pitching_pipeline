#!/usr/bin/env python3
"""
Utilities for storing and retrieving pitcher data
"""

import sqlite3
import pandas as pd
from datetime import datetime
from .common import logger, pitcher_column_mapping

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
        
        # Fix missing dates - replace empty or None values in date_game column
        if 'date_game' in df_copy.columns:
            # Get years for each row to use in placeholder dates
            years = df_copy['year'].fillna(datetime.now().year).astype(int)
            
            # Print date values for debugging
            logger.debug(f"Date values for {player_id} before cleaning: {df_copy['date_game'].tolist()[:5]}...")
            
            # Create a mask for missing dates
            missing_dates = df_copy['date_game'].isna() | (df_copy['date_game'] == '') | (df_copy['date_game'].str.lower() == 'none')
            
            # For rows with missing dates, create placeholder dates using the year from that row
            for idx in df_copy[missing_dates].index:
                year = years.loc[idx]
                df_copy.loc[idx, 'date_game'] = f"{year}-01-01"
            
            # Additional check - ensure ALL dates have a value
            df_copy['date_game'] = df_copy.apply(
                lambda row: f"{row['year']}-01-01" if pd.isna(row['date_game']) or row['date_game'] == '' 
                else row['date_game'], 
                axis=1
            )
            
            # Log how many dates needed fixing
            num_fixed = missing_dates.sum()
            if num_fixed > 0:
                logger.warning(f"Fixed {num_fixed} missing date values for {player_id}")
            
            # Print date values for debugging
            logger.debug(f"Date values for {player_id} after cleaning: {df_copy['date_game'].tolist()[:5]}...")
        
        # Handle road_indicator (convert non-null values to 1)
        if 'road_indicator' in df_copy.columns:
            logger.debug(f"Road indicator values before conversion: {df_copy['road_indicator'].tolist()[:5]}...")
            # Convert non-null values to 1 (indicating road game)
            df_copy['road_indicator'] = df_copy['road_indicator'].apply(
                lambda x: 1 if pd.notna(x) and x == '@' else 0
            )
            logger.debug(f"Road indicator values after conversion: {df_copy['road_indicator'].tolist()[:5]}...")
        
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
        
        # Print dtypes for debugging
        logger.debug(f"DataFrame column dtypes before SQL insert: {df_filtered.dtypes}")
        
        # Insert data into database
        df_filtered.to_sql('pitching_gamelogs', conn, if_exists='append', index=False)
        
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