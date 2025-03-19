#!/usr/bin/env python3
"""
Database schema definitions and creation functions
"""

import os
import sqlite3
from .common import logger

def create_database(db_path="baseball.db", force_recreate=False):
    """
    Create SQLite database and tables if they don't exist
    
    Args:
        db_path (str): Path to the database file
        force_recreate (bool): Whether to drop and recreate existing tables
        
    Returns:
        str: Path to the created database
    """
    db_path = os.path.abspath(db_path)
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path) or '.', exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Drop tables if force_recreate is True
        if force_recreate:
            cursor.execute("DROP TABLE IF EXISTS pitching_gamelogs")
            cursor.execute("DROP TABLE IF EXISTS team_stats")
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
            fip REAL,
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
            run_expectancy_24 REAL,
            draftkings_points REAL,
            fanduel_points REAL,
            career_game_num INTEGER,
            road_indicator INTEGER,
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
        
        # Create the team_stats table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id TEXT NOT NULL,
            year INTEGER NOT NULL,
            games INTEGER,
            runs_per_game REAL,
            plate_appearances INTEGER,
            at_bats INTEGER,
            runs INTEGER,
            hits INTEGER,
            doubles INTEGER,
            triples INTEGER,
            home_runs INTEGER,
            rbi INTEGER,
            stolen_bases INTEGER,
            caught_stealing INTEGER,
            walks INTEGER,
            strikeouts INTEGER,
            batting_avg REAL,
            on_base_pct REAL,
            slugging_pct REAL,
            ops REAL,
            ops_plus INTEGER,
            total_bases INTEGER,
            gidp INTEGER,
            hit_by_pitch INTEGER,
            sacrifice_hits INTEGER,
            sacrifice_flies INTEGER,
            intentional_walks INTEGER,
            UNIQUE(team_id, year)
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