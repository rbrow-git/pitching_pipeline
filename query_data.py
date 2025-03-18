#!/usr/bin/env python3
"""
Query data from the baseball SQLite database
"""

import sqlite3
import pandas as pd
import argparse


def query_player_data(player_id, db_path="baseball.db"):
    """Query and display data for a specific player"""
    conn = sqlite3.connect(db_path)
    
    # Show player summary
    query = """
    SELECT 
        player_id,
        COUNT(*) as games,
        SUM(CAST(innings_pitched AS REAL)) as total_innings,
        SUM(strikeouts) as total_strikeouts,
        ROUND(AVG(strikeouts), 1) as avg_strikeouts_per_game,
        SUM(walks) as total_walks,
        SUM(hits) as total_hits,
        SUM(earned_runs) as total_earned_runs,
        ROUND(AVG(era), 2) as avg_era
    FROM pitching_gamelogs
    WHERE player_id = ?
    GROUP BY player_id
    """
    
    summary_df = pd.read_sql_query(query, conn, params=(player_id,))
    if summary_df.empty:
        print(f"No data found for player {player_id}")
        return
    
    print(f"\nSummary for {player_id}:")
    print(summary_df.to_string(index=False))
    
    # Show individual games
    query = """
    SELECT 
        year, 
        game_date,
        innings_pitched,
        hits,
        runs,
        earned_runs,
        walks,
        strikeouts,
        home_runs,
        era,
        game_result
    FROM pitching_gamelogs
    WHERE player_id = ?
    ORDER BY year, game_date
    """
    
    games_df = pd.read_sql_query(query, conn, params=(player_id,))
    
    print(f"\nGame log for {player_id} ({len(games_df)} games):")
    pd.set_option('display.max_rows', 20)
    print(games_df)
    
    conn.close()


def list_players(db_path="baseball.db"):
    """List all players in the database"""
    conn = sqlite3.connect(db_path)
    
    query = """
    SELECT 
        p.player_id,
        p.last_updated,
        COUNT(g.id) as games,
        MIN(g.year) as first_year,
        MAX(g.year) as last_year
    FROM players p
    LEFT JOIN pitching_gamelogs g ON p.player_id = g.player_id
    GROUP BY p.player_id
    ORDER BY p.player_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("No players found in the database")
        return
    
    print("\nPlayers in database:")
    print(df.to_string(index=False))


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Query baseball data from SQLite database')
    parser.add_argument('--player-id', help='Player ID to query')
    parser.add_argument('--list-players', action='store_true', help='List all players in the database')
    parser.add_argument('--db-path', default='baseball.db', help='Path to SQLite database file')
    
    args = parser.parse_args()
    
    if args.list_players:
        list_players(args.db_path)
    elif args.player_id:
        query_player_data(args.player_id, args.db_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 