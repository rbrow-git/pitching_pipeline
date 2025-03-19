#!/usr/bin/env python3
"""
Database utilities for storing pitcher game logs in SQLite
"""

import sqlite3
import os
import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define column mapping between scraped data and database
column_mapping = {
    # Core metadata
    'player_id': 'player_id',
    'year': 'year',
    'date_game': 'date_game',
    
    # Team info
    'team_ID': 'team_id',
    'opp_ID': 'opponent_id',
    'game_result': 'game_result',
    
    # Basic pitching stats
    'IP': 'innings_pitched',
    'H': 'hits',
    'R': 'runs',
    'ER': 'earned_runs',
    'BB': 'walks',
    'SO': 'strikeouts',
    'HR': 'home_runs',
    'HBP': 'hit_by_pitch',
    
    # Advanced metrics
    'earned_run_avg': 'era',
    'fip': 'fip',
    'batters_faced': 'batters_faced',
    'game_score': 'game_score',
    
    # Pitch data
    'pitches': 'pitches',
    'strikes_total': 'strikes',
    'strikes_looking': 'strikes_looking',
    'strikes_swinging': 'strikes_swinging',
    
    # Batted ball data
    'inplay_gb_total': 'ground_balls',
    'inplay_fb_total': 'fly_balls',
    'inplay_ld': 'line_drives',
    'inplay_pu': 'pop_ups',
    'inplay_unk': 'unknown_batted_balls',
    
    # Base runners
    'SB': 'stolen_bases',
    'CS': 'caught_stealing',
    'pickoffs': 'pickoffs',
    
    # Opponent batting
    'AB': 'at_bats',
    '2B': 'doubles',
    '3B': 'triples',
    'IBB': 'intentional_walks',
    'GIDP': 'grounded_into_double_play',
    'SF': 'sacrifice_flies',
    'ROE': 'reached_on_error',
    
    # Win Probability metrics
    'leverage_index_avg': 'average_leverage_index',
    'wpa_def': 'win_probability_added',
    'cli_avg': 'clutch_leverage_index',
    'cwpa_def': 'championship_win_probability_added',
    're24_def': 'run_expectancy_24',
    
    # Fantasy
    'draftkings_points': 'draftkings_points',
    'fanduel_points': 'fanduel_points',
}


def create_database(db_path="baseball.db", force_recreate=False):
    """Create SQLite database and tables if they don't exist"""
    db_path = os.path.abspath(db_path)
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop tables if force_recreate is True
        if force_recreate:
            cursor.execute("DROP TABLE IF EXISTS pitching_gamelogs")
            cursor.execute("DROP TABLE IF EXISTS players")
            logger.info("Dropped existing tables")
        
        # Create the pitching_gamelogs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pitching_gamelogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT NOT NULL,
            date_game TEXT NOT NULL,
            year INTEGER NOT NULL,
            team_id TEXT,
            opponent_id TEXT,
            game_result TEXT,
            innings_pitched REAL,
            hits INTEGER,
            runs INTEGER,
            earned_runs INTEGER,
            walks INTEGER,
            strikeouts INTEGER,
            home_runs INTEGER,
            hit_by_pitch INTEGER,
            era REAL,
            batters_faced INTEGER,
            pitches INTEGER,
            strikes INTEGER,
            strikes_looking INTEGER,
            strikes_swinging INTEGER,
            ground_balls INTEGER,
            fly_balls INTEGER,
            line_drives INTEGER,
            pop_ups INTEGER,
            unknown_batted_balls INTEGER,
            game_score INTEGER,
            stolen_bases INTEGER,
            caught_stealing INTEGER,
            pickoffs INTEGER,
            at_bats INTEGER,
            doubles INTEGER,
            triples INTEGER,
            intentional_walks INTEGER,
            grounded_into_double_play INTEGER,
            sacrifice_flies INTEGER,
            reached_on_error INTEGER,
            win_probability_added REAL,
            average_leverage_index REAL,
            clutch_leverage_index REAL,
            championship_win_probability_added REAL,
            run_expectancy_24 REAL,
            draftkings_points REAL,
            fanduel_points REAL,
            UNIQUE(player_id, date_game)
        )
        """)
        
        # Create the players table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            player_name TEXT,
            last_updated TEXT
        )
        """)
        
        conn.commit()
        logger.debug(f"Database created at {db_path}")
        return db_path
    
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None
    
    finally:
        if conn:
            conn.close()


def store_pitcher_data(df, player_id, db_path="baseball.db", player_name=None):
    """Store pitcher data into SQLite database"""
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
        df_copy = df_copy.rename(columns={k: v for k, v in column_mapping.items() if k in df_copy.columns})
        
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
    """Update a player's name in the database"""
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
    """Retrieve pitcher data from the database"""
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
    """Retrieve all pitcher data from the database"""
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
    """Get list of player IDs already in the database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT player_id, player_name FROM players")
        players = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        return players
    except:
        return {} 