#!/usr/bin/env python3
"""
Common utilities and definitions for database operations
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
pitcher_column_mapping = {
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
    'career_game_num': 'career_game_num',
    'team_homeORaway': 'road_indicator',
    
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
    're24_def': 'run_expectancy_24',
    
    # Fantasy
    'draftkings_points': 'draftkings_points',
    'fanduel_points': 'fanduel_points',
}

# Team stats column mapping
team_column_mapping = {
    'Team': 'team_id',
    'year': 'year',
    'G': 'games',
    'R/G': 'runs_per_game',
    'PA': 'plate_appearances',
    'AB': 'at_bats',
    'R': 'runs',
    'H': 'hits',
    '2B': 'doubles',
    '3B': 'triples',
    'HR': 'home_runs',
    'RBI': 'rbi',
    'SB': 'stolen_bases',
    'CS': 'caught_stealing',
    'BB': 'walks',
    'SO': 'strikeouts',
    'BA': 'batting_avg',
    'OBP': 'on_base_pct',
    'SLG': 'slugging_pct',
    'OPS': 'ops',
    'OPS+': 'ops_plus',
    'TB': 'total_bases',
    'GDP': 'gidp',
    'HBP': 'hit_by_pitch',
    'SH': 'sacrifice_hits',
    'SF': 'sacrifice_flies',
    'IBB': 'intentional_walks'
} 