#!/usr/bin/env python3
"""
Utilities for storing and retrieving team statistics
"""

import sqlite3
import pandas as pd
from .common import logger, team_column_mapping

def store_team_stats(df, db_path="baseball.db"):
    """
    Store team stats into the SQLite database
    
    Args:
        df (DataFrame): Team stats dataframe
        db_path (str): Path to SQLite database
        
    Returns:
        bool: Success or failure
    """
    if df is None or df.empty:
        logger.warning("No team stats data to store")
        return False
    
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        
        # Rename DataFrame columns to match database schema
        df_copy = df.copy()
        df_copy = df_copy.rename(columns={k: v for k, v in team_column_mapping.items() if k in df_copy.columns})
        
        # Insert or replace data
        total_teams = 0
        for _, row in df_copy.iterrows():
            fields = []
            values = []
            
            for col in row.index:
                if pd.notna(row[col]):
                    fields.append(col)
                    values.append(row[col])
            
            # Create placeholders for the values
            placeholders = ', '.join(['?' for _ in values])
            
            # Construct SQL query
            fields_str = ', '.join(fields)
            sql = f"INSERT OR REPLACE INTO team_stats ({fields_str}) VALUES ({placeholders})"
            
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql, values)
            total_teams += 1
        
        conn.commit()
        logger.info(f"Successfully stored {total_teams} team records in database")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database error storing team stats: {e}")
        return False
    
    except Exception as e:
        logger.error(f"Error storing team stats: {e}")
        return False
    
    finally:
        if conn:
            conn.close()


def get_team_stats(team_id=None, year=None, db_path="baseball.db"):
    """
    Retrieve team stats from the database
    
    Args:
        team_id (str): Team ID to filter by, or None for all teams
        year (int): Year to filter by, or None for all years
        db_path (str): Path to database
        
    Returns:
        DataFrame: DataFrame with team statistics
    """
    try:
        conn = sqlite3.connect(db_path)
        
        # Construct query based on filters
        query = "SELECT * FROM team_stats"
        params = []
        
        if team_id or year:
            query += " WHERE"
            
            if team_id:
                query += " team_id = ?"
                params.append(team_id)
                
                if year:
                    query += " AND year = ?"
                    params.append(year)
            elif year:
                query += " year = ?"
                params.append(year)
        
        # Add order by clause
        query += " ORDER BY year DESC, team_id"
        
        # Execute query
        df = pd.read_sql_query(query, conn, params=params)
        return df
    
    except Exception as e:
        logger.error(f"Error retrieving team stats: {str(e)}")
        return None
    
    finally:
        if conn:
            conn.close()


def get_team_ids(db_path="baseball.db"):
    """
    Get list of team IDs in the database
    
    Args:
        db_path (str): Path to database
        
    Returns:
        list: List of unique team IDs
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT team_id FROM team_stats ORDER BY team_id")
        team_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return team_ids
    except:
        return [] 