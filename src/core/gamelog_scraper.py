#!/usr/bin/env python3
"""
Module for scraping baseball-reference.com game logs for pitchers
"""

from scrapling import StealthyFetcher
import pandas as pd
import time
import re
from datetime import datetime
from io import StringIO
from src.core.logging.config import get_logger
import logging

# Get logger for this module
logger = get_logger(__name__)

# Stats to extract from the game logs
STATS_TO_EXTRACT = [
    # Core metadata
    'career_game_num',
    'date_game',
    
    # Team info
    'team_ID',
    'team_homeORaway',  # Home/away indicator - '@' for away games, None for home games
    'opp_ID',
    'game_result', 
    
    # Basic pitching stats
    'IP',
    'H',
    'R',
    'ER', 
    'BB',
    'SO',
    'HR',
    'HBP',
    
    # Advanced metrics
    'earned_run_avg',
    'fip',
    'batters_faced',
    'game_score',
    
    # Pitch data
    'pitches',
    'strikes_total',
    'strikes_looking',
    'strikes_swinging',
    
    # Batted ball data
    'inplay_gb_total',
    'inplay_fb_total',
    'inplay_ld',
    'inplay_pu',
    'inplay_unk',
    
    # Base runners
    'SB',
    'CS',
    'pickoffs',
    
    # Opponent batting
    'AB',
    '2B',
    '3B',
    'IBB',
    'GIDP',
    'SF',
    'ROE',
    
    # Win Probability metrics
    'leverage_index_avg',
    'wpa_def',
    'cli_avg',
    're24_def',
    
    # Fantasy
    'draftkings_points',
    'fanduel_points',
]


def extract_player_name(page):
    """
    Extract player name from the Baseball Reference page using breadcrumbs
    
    Args:
        page: The HTML page response from scrapling
        
    Returns:
        str: The player's full name or None if not found
    """
    try:
        # Extract player name from breadcrumbs (most reliable method)
        breadcrumbs = page.css('div[itemtype*="BreadcrumbList"]')
        if breadcrumbs:
            items = breadcrumbs.css('[itemprop="itemListElement"]')
            # The player name is usually the last breadcrumb item
            if items and len(items) >= 3:  # Usually has Home > Players > Player Name
                last_item = items[-1]
                name_elem = last_item.css_first('[itemprop="name"]')
                if name_elem:
                    player_name = name_elem.text.clean()
                    logger.debug(f"Extracted player name from breadcrumbs: {player_name}")
                    return player_name
        
        # Fallback method using h1 with Game Logs text
        for h1 in page.css('h1'):
            h1_text = h1.text.clean()
            if 'Game Logs' in h1_text:
                player_part = h1_text.split('Game Logs')[0].strip()
                # Remove any trailing year or characters
                player_part = re.sub(r'\d+\s*$', '', player_part).strip()
                logger.debug(f"Extracted player name from h1: {player_part}")
                return player_part
            
        logger.warning("Could not extract player name from page")
        return None
    except Exception as e:
        logger.error(f"Error extracting player name: {str(e)}")
        return None


def scrape_year(player_id, year, retry_limit=3):
    """
    Scrape pitching game logs for a player for a specific year
    
    Args:
        player_id (str): Baseball Reference player ID
        year (int): Year to scrape
        retry_limit (int): Number of retries on failure
        
    Returns:
        tuple: (DataFrame, str) containing game logs and player name, or (None, None) if error
    """
    # The URL pattern for pitching game logs
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=p&year={year}"
    
    # Initialize the fetcher
    fetcher = StealthyFetcher()
    
    attempts = 0
    while attempts < retry_limit:
        attempts += 1
        logger.debug(f"Fetching {player_id} year {year} (attempt {attempts})")
        
        # Fetch with a retry
        response = fetcher.fetch(url)
        
        if not response:
            logger.warning(f"Failed to fetch {url} (attempt {attempts}/{retry_limit})")
            time.sleep(2 ** attempts)  # Exponential backoff
            continue  # Try again
    
        # Extract player name from the page title
        player_name = None
        title_match = re.search(r'<title>(.+?) MLB Pitcher Game Log', str(response.html_content))
        if title_match:
            player_name = title_match.group(1).strip()
        
        # Look for the standard game log table
        game_log_match = re.search(r'(<table[^>]*?id="pitching_gamelogs"[^>]*?>.*?</table>)', str(response.html_content), re.DOTALL)
        
        if not game_log_match:
            logger.debug(f"No game log table found for {player_id} in {year}")
            # Player might not have pitched that year
            return None, player_name
        
        game_log_html = game_log_match.group(1)
        
        try:
            # Use pandas to parse the HTML table
            dfs = pd.read_html(StringIO(game_log_html))
            
            if not dfs or len(dfs) == 0:
                logger.warning(f"No data found in game log table for {player_id} in {year}")
                return None, player_name
                
            df = dfs[0]
            
            # Process the dataframe
            df = process_game_log_df(df, player_id, year)
            
            if df is not None and not df.empty:
                logger.debug(f"Successfully scraped {len(df)} games for {player_id} in {year}")
                
                # Log the first game to verify data
                if not df.empty and logger.isEnabledFor(logging.DEBUG):
                    first_game = df.iloc[0].to_dict()
                    logger.debug(f"First game sample: {first_game}")
                
                return df, player_name
        
        except Exception as e:
            logger.error(f"Error processing game log for {player_id} in {year}: {str(e)}")
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"HTML snippet: {game_log_html[:500]}...")
            time.sleep(2 ** attempts)  # Exponential backoff
            continue  # Try again
    
    logger.error(f"Failed to scrape {player_id} year {year} after {retry_limit} attempts")
    return None, None


def process_game_log_df(df, player_id, year):
    """
    Process the raw game log dataframe into a clean format
    
    Args:
        df (DataFrame): Raw game log dataframe
        player_id (str): Baseball Reference player ID
        year (int): Year being scraped
        
    Returns:
        DataFrame: Processed dataframe with cleaned columns
    """
    # Check if this is a summary/multi-header df
    if 'Rk' not in df.columns and df.shape[0] > 0:
        # Handle multi-header tables by getting the second row of headers
        # This happens when there are two header rows in the table
        if isinstance(df.columns, pd.MultiIndex):
            # Get the second level of column names
            df.columns = df.columns.get_level_values(1)
        else:
            # Skip the first row (which is a second header)
            df = df.iloc[1:].reset_index(drop=True)
            df.columns = df.iloc[0]
            df = df.iloc[1:].reset_index(drop=True)
    
    # First, filter rows that are actual games (have a rank number)
    if 'Rk' in df.columns:
        df = df[df['Rk'].notna() & (df['Rk'] != 'Rk')]
    else:
        logger.warning(f"No 'Rk' column found in dataframe for {player_id} in {year}")
        return None
    
    # Filter out non-game rows
    if 'Gtm' in df.columns:  # Game team column, only used in newer tables
        df = df[df['Gtm'].notna()]
    elif 'Gcar' in df.columns:  # Career game column
        df = df[df['Gcar'].notna()]
    
    # Filter out rows with missing or invalid date
    if 'Date' in df.columns:
        df = df[df['Date'].notna() & (df['Date'] != '')]
    
    # Skip if no games found
    if df.empty:
        logger.info(f"No games found for {player_id} in {year} after filtering")
        return df
    
    # Add player_id and year columns
    df['player_id'] = player_id
    df['year'] = year
    
    # Rename columns to more consistent names
    rename_map = {
        'Rk': 'game_num',
        'Gcar': 'career_game_num',
        'Gtm': 'team_game_num',
        'Date': 'date_game',
        'Tm': 'team_ID',
        'Opp': 'opp_ID',
        'Rslt': 'game_result',
        '@': 'team_homeORaway',
        'IP': 'IP',
        'H': 'H',
        'R': 'R',
        'ER': 'ER',
        'BB': 'BB',
        'SO': 'SO',
        'HR': 'HR',
        'HBP': 'HBP',
        'ERA': 'earned_run_avg',
        'FIP': 'fip',
        'BF': 'batters_faced',
        'Pit': 'pitches',
        'Str': 'strikes_total',
        'StL': 'strikes_looking',
        'StS': 'strikes_swinging',
        'GB': 'inplay_gb_total',
        'FB': 'inplay_fb_total',
        'LD': 'inplay_ld',
        'PU': 'inplay_pu',
        'Unk': 'inplay_unk',
        'GSc': 'game_score',
        'SB': 'SB',
        'CS': 'CS',
        'PO': 'pickoffs',
        'AB': 'AB',
        '2B': '2B',
        '3B': '3B',
        'IBB': 'IBB',
        'GDP': 'GIDP',
        'SF': 'SF',
        'ROE': 'ROE',
        'aLI': 'leverage_index_avg',
        'WPA': 'wpa_def',
        'cLI': 'cli_avg',
        'RE24': 're24_def',
        'DK': 'draftkings_points',
        'FD': 'fanduel_points',
    }
    
    # Apply the rename mapping
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    
    # Select only the columns we want
    df = df[[col for col in STATS_TO_EXTRACT + ['player_id', 'year'] if col in df.columns]]
    
    # Clean up numeric columns
    for col in df.columns:
        if col not in ['player_id', 'date_game', 'team_ID', 'opp_ID', 'game_result', 'team_homeORaway', 'year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df


def scrape_player(player_id, years=None):
    """
    Scrape pitching game logs for a player for multiple years
    
    Args:
        player_id (str): Baseball Reference player ID
        years (list): List of years to scrape, or None for years 2021-2024
    
    Returns:
        tuple: (DataFrame, str) containing combined game logs and player name, or (None, None) if error
    """
    if not years:
        current_year = datetime.now().year
        years = list(range(2021, current_year))  # Exclude current year
    
    all_data = []
    player_name = None
    
    for year in years:
        df, name = scrape_year(player_id, year)
        if df is not None and not df.empty:
            all_data.append(df)
            # Set player_name if we found it and don't have it yet
            if name and not player_name:
                player_name = name
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        logger.info(f"Combined data for {player_id}: {len(combined_df)} games across {len(years)} seasons")
        return combined_df, player_name
    else:
        logger.warning(f"No data found for {player_id}")
        return None, player_name 