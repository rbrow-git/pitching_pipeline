#!/usr/bin/env python3
"""
Database utilities for storing pitcher game logs in SQLite
"""

import sqlite3
import os
import pandas as pd


def create_database(db_path="baseball.db", force_recreate=False):
    """Create SQLite database and tables if they don't exist"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if we need to recreate tables
    if force_recreate:
        cursor.execute("DROP TABLE IF EXISTS pitching_gamelogs")
        cursor.execute("DROP TABLE IF EXISTS players")
    
    # Check if tables exist and have correct structure
    cursor.execute("PRAGMA table_info(pitching_gamelogs)")
    columns = {row[1]: row for row in cursor.fetchall()}
    
    # If table exists but missing required columns, drop and recreate
    if columns and ('date_game' not in columns or 'team_homeORaway' not in columns):
        print("Existing database schema is outdated. Recreating tables...")
        cursor.execute("DROP TABLE IF EXISTS pitching_gamelogs")
        columns = {}
    
    # Create pitching_gamelogs table if needed
    if not columns:
        # Create pitching_gamelogs table with expanded columns to match Baseball Reference
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pitching_gamelogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT NOT NULL,
            year INTEGER NOT NULL,
            date_game TEXT,
            career_game_num TEXT,
            team_game_num TEXT,
            team_id TEXT,
            team_homeORaway TEXT,
            opponent_id TEXT,
            game_result TEXT,
            player_game_span TEXT,
            player_game_result TEXT,
            days_rest INTEGER,
            innings_pitched TEXT,
            hits INTEGER,
            runs INTEGER,
            earned_runs INTEGER,
            walks INTEGER,
            strikeouts INTEGER,
            home_runs INTEGER,
            hit_by_pitch INTEGER,
            era REAL,
            fip REAL,
            batters_faced INTEGER,
            pitches INTEGER,
            strikes_total INTEGER,
            strikes_looking INTEGER,
            strikes_swinging INTEGER,
            ground_balls INTEGER,
            fly_balls INTEGER,
            line_drives INTEGER,
            pop_ups INTEGER,
            unknown_batted_balls INTEGER,
            game_score INTEGER,
            inherited_runners INTEGER,
            inherited_score INTEGER,
            stolen_bases INTEGER,
            caught_stealing INTEGER,
            pickoffs INTEGER,
            at_bats INTEGER,
            doubles INTEGER,
            triples INTEGER,
            intentional_walks INTEGER,
            double_plays INTEGER,
            sacrifice_flies INTEGER,
            reached_on_error INTEGER,
            leverage_index REAL,
            win_probability_added REAL,
            championship_leverage_index REAL,
            championship_win_probability_added TEXT,
            run_expectancy_24 TEXT,
            situation_in TEXT,
            situation_out TEXT,
            
            /* Add index for faster queries */
            UNIQUE(player_id, year, career_game_num)
        )
        ''')
    else:
        # Check for and add missing columns if needed
        missing_columns = []
        for col in ['team_homeORaway', 'player_game_span', 'player_game_result', 'days_rest']:
            if col not in columns:
                col_type = 'INTEGER' if col == 'days_rest' else 'TEXT'
                missing_columns.append((col, col_type))
        
        for col_name, col_type in missing_columns:
            try:
                cursor.execute(f"ALTER TABLE pitching_gamelogs ADD COLUMN {col_name} {col_type}")
                print(f"Added missing column '{col_name}' to pitching_gamelogs table")
            except sqlite3.OperationalError as e:
                print(f"Error adding column {col_name}: {str(e)}")
    
    # Check if players table exists
    cursor.execute("PRAGMA table_info(players)")
    player_columns = {row[1]: row for row in cursor.fetchall()}
    
    if not player_columns:
        # Create players table with player_name column
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            player_name TEXT,
            last_updated TEXT
        )
        ''')
    elif 'player_name' not in player_columns:
        # Add player_name column if it doesn't exist
        try:
            cursor.execute("ALTER TABLE players ADD COLUMN player_name TEXT")
            print("Added player_name column to players table")
        except sqlite3.OperationalError as e:
            print(f"Error adding player_name column: {str(e)}")
    
    conn.commit()
    conn.close()
    
    return db_path


def store_pitcher_data(df, player_id, db_path="baseball.db", player_name=None):
    """Store pitcher data into SQLite database"""
    if df is None or df.empty:
        return False
    
    conn = sqlite3.connect(db_path)
    
    # Standardize column names that we want to store - expanded mapping
    column_mapping = {
        'player_id': 'player_id', 
        'year': 'year',
        'date_game': 'date_game',
        'career_game_num': 'career_game_num',
        'team_game_num': 'team_game_num',
        'team_ID': 'team_id',
        'team_homeORaway': 'team_homeORaway',
        'opp_ID': 'opponent_id',
        'game_result': 'game_result',
        'player_game_span': 'player_game_span',
        'player_game_result': 'player_game_result',
        'days_rest': 'days_rest',
        'IP': 'innings_pitched',
        'H': 'hits',
        'R': 'runs',
        'ER': 'earned_runs',
        'BB': 'walks',
        'SO': 'strikeouts',
        'HR': 'home_runs',
        'HBP': 'hit_by_pitch',
        'earned_run_avg': 'era',
        'fip': 'fip',
        'batters_faced': 'batters_faced',
        'pitches': 'pitches',
        'strikes_total': 'strikes_total',
        'strikes_looking': 'strikes_looking',
        'strikes_swinging': 'strikes_swinging',
        'inplay_gb_total': 'ground_balls',
        'inplay_fb_total': 'fly_balls',
        'inplay_ld': 'line_drives',
        'inplay_pu': 'pop_ups',
        'inplay_unk': 'unknown_batted_balls',
        'game_score': 'game_score',
        'inherited_runners': 'inherited_runners',
        'inherited_score': 'inherited_score',
        'SB': 'stolen_bases',
        'CS': 'caught_stealing',
        'pickoffs': 'pickoffs',
        'AB': 'at_bats',
        '2B': 'doubles',
        '3B': 'triples',
        'IBB': 'intentional_walks',
        'GIDP': 'double_plays',
        'SF': 'sacrifice_flies',
        'ROE': 'reached_on_error',
        'leverage_index_avg': 'leverage_index',
        'wpa_def': 'win_probability_added',
        'cli_avg': 'championship_leverage_index',
        'cwpa_def': 'championship_win_probability_added',
        're24_def': 'run_expectancy_24',
        'pitcher_situation_in': 'situation_in',
        'pitcher_situation_out': 'situation_out'
    }
    
    # Create a copy of the dataframe to avoid modifying the original
    df_to_store = df.copy()
    
    # Print available columns for debugging
    print(f"Available columns: {', '.join(df_to_store.columns)}")
    
    # Rename columns according to the mapping
    columns_to_rename = {old: new for old, new in column_mapping.items() if old in df_to_store.columns}
    df_to_store = df_to_store.rename(columns=columns_to_rename)
    
    # Convert numeric columns 
    numeric_columns = [
        'days_rest', 'hits', 'runs', 'earned_runs', 'walks', 'strikeouts', 'home_runs', 'hit_by_pitch',
        'era', 'fip', 'batters_faced', 'pitches', 'strikes_total', 'strikes_looking',
        'strikes_swinging', 'ground_balls', 'fly_balls', 'line_drives', 'pop_ups',
        'unknown_batted_balls', 'game_score', 'inherited_runners', 'inherited_score',
        'stolen_bases', 'caught_stealing', 'pickoffs', 'at_bats', 'doubles', 'triples',
        'intentional_walks', 'double_plays', 'sacrifice_flies', 'reached_on_error',
        'leverage_index', 'win_probability_added', 'championship_leverage_index'
    ]
    
    for col in numeric_columns:
        if col in df_to_store.columns:
            df_to_store[col] = pd.to_numeric(df_to_store[col], errors='coerce')
    
    # Keep only columns in our database schema
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(pitching_gamelogs)")
    db_columns = [row[1] for row in cursor.fetchall()]
    
    # Filter data to only include columns that exist in the database
    columns_to_keep = [col for col in df_to_store.columns if col in db_columns]
    if len(columns_to_keep) < len(df_to_store.columns):
        missing_cols = set(df_to_store.columns) - set(columns_to_keep)
        print(f"Warning: Some columns from scraped data will not be stored in the database.")
        print(f"Available columns in dataframe: {len(df_to_store.columns)}, columns in database: {len(columns_to_keep)}")
        print(f"Missing columns: {', '.join(missing_cols)}")
    
    df_to_store = df_to_store[columns_to_keep]
    
    # Insert data using pandas to_sql with conflict resolution
    try:
        # Store data in the gamelogs table
        df_to_store.to_sql('pitching_gamelogs', conn, if_exists='append', index=False)
        
        # Update the players table with the current timestamp and player name if provided
        cursor = conn.cursor()
        if player_name:
            cursor.execute(
                "INSERT OR REPLACE INTO players (player_id, player_name, last_updated) VALUES (?, ?, datetime('now'))",
                (player_id, player_name)
            )
        else:
            # Check if we already have a player_name before overwriting it with NULL
            cursor.execute("SELECT player_name FROM players WHERE player_id = ?", (player_id,))
            existing_name = cursor.fetchone()
            
            if existing_name and existing_name[0]:
                # Keep existing name
                cursor.execute(
                    "UPDATE players SET last_updated = datetime('now') WHERE player_id = ?",
                    (player_id,)
                )
            else:
                # No existing name, just update without a name
                cursor.execute(
                    "INSERT OR REPLACE INTO players (player_id, last_updated) VALUES (?, datetime('now'))",
                    (player_id,)
                )
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error storing data for {player_id}: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()


def update_player_name(player_id, player_name, db_path="baseball.db"):
    """Update a player's name in the database"""
    if not player_id or not player_name:
        return False
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE players SET player_name = ? WHERE player_id = ?",
            (player_name, player_id)
        )
        
        if cursor.rowcount == 0:
            # Player doesn't exist yet, insert a new record
            cursor.execute(
                "INSERT INTO players (player_id, player_name, last_updated) VALUES (?, ?, datetime('now'))",
                (player_id, player_name)
            )
            
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating player name for {player_id}: {str(e)}")
        return False


def get_stored_pitcher_data(player_id, db_path="baseball.db"):
    """Retrieve pitcher data from the database"""
    conn = sqlite3.connect(db_path)
    
    query = """
    SELECT g.*, p.player_name 
    FROM pitching_gamelogs g
    LEFT JOIN players p ON g.player_id = p.player_id
    WHERE g.player_id = ?
    ORDER BY g.year, g.date_game
    """
    
    df = pd.read_sql_query(query, conn, params=(player_id,))
    conn.close()
    
    return df if not df.empty else None


def get_all_pitcher_data(db_path="baseball.db"):
    """Retrieve all pitcher data from the database"""
    conn = sqlite3.connect(db_path)
    
    query = """
    SELECT g.*, p.player_name 
    FROM pitching_gamelogs g
    LEFT JOIN players p ON g.player_id = p.player_id
    ORDER BY g.player_id, g.year, g.date_game
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df if not df.empty else None


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