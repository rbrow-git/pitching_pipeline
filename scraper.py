#!/usr/bin/env python3
"""
Module for scraping baseball-reference.com game logs
"""

from scrapling import StealthyFetcher
import pandas as pd
import logging
import time
import re
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
                    logger.info(f"Extracted player name from breadcrumbs: {player_name}")
                    return player_name
        
        # Fallback method using h1 with Game Logs text
        for h1 in page.css('h1'):
            h1_text = h1.text.clean()
            if 'Game Logs' in h1_text:
                player_part = h1_text.split('Game Logs')[0].strip()
                # Remove any trailing year or characters
                player_part = re.sub(r'\d+\s*$', '', player_part).strip()
                logger.info(f"Extracted player name from h1: {player_part}")
                return player_part
            
        logger.warning("Could not extract player name from page")
        return None
    except Exception as e:
        logger.error(f"Error extracting player name: {str(e)}")
        return None


def scrape_year(player_id, year, retry_limit=3, retry_delay=2):
    """
    Scrape pitching game logs for a player for a specific year
    
    Args:
        player_id (str): Baseball Reference player ID
        year (int): Year to scrape
        retry_limit (int): Number of retries on failure
        retry_delay (int): Delay between retries in seconds
    
    Returns:
        tuple: (DataFrame, str) containing game logs and player name or (None, None) if error
    """
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={player_id}&t=p&year={year}"
    logger.info(f"Fetching data for player {player_id} year {year} from {url}")
    
    attempts = 0
    while attempts < retry_limit:
        try:
            # Initialize the Scrapling fetcher with stealth mode to avoid bot detection
            fetcher = StealthyFetcher()
            response = fetcher.fetch(
                url,
                headless=True,
                disable_resources=True,
                timeout=90000,
            )
            
            if response.status != 200:
                logger.error(f"Failed to fetch {url}: Status {response.status}")
                attempts += 1
                time.sleep(retry_delay)
                continue
            
            # Parse HTML content
            page = response
            
            # Extract player name from the page
            player_name = extract_player_name(page)
            
            # Find the main pitching game logs table
            table = page.css_first('#pitching_gamelogs')
            if not table:
                logger.error(f"Could not find pitching game logs table for {player_id} year {year}")
                return None, player_name
            
            # Extract all rows - we'll filter out the ones we don't want later
            rows = table.css('tr')
            
            data = []
            headers = []
            
            # Find the header row which has the th elements
            header_row = table.css_first('thead tr')
            if not header_row:
                logger.error(f"Could not find header row for {player_id} year {year}")
                return None, player_name
            
            # Extract headers from the header row
            for th in header_row.css('th[data-stat]'):
                data_stat = th.attrib.get('data-stat')
                if data_stat:
                    headers.append(data_stat)
            
            # Extract data rows - skip header rows and any row with class="thead"
            for row in table.css('tbody tr'):
                # Skip header rows
                if row.has_class('thead') or row.has_class('spacer'):
                    continue
                    
                # Skip if no data-stat elements
                cells = row.css('td[data-stat]')
                if not cells:
                    continue
                
                row_data = {}
                
                # Add metadata
                row_data['player_id'] = player_id
                row_data['year'] = year
                
                # Extract cell data for each column
                for cell in cells:
                    data_stat = cell.attrib.get('data-stat')
                    
                    # Special handling for date field - extract actual date from link if available
                    if data_stat == 'date_game':
                        # Try to get the link element
                        date_link = cell.css_first('a')
                        if date_link and 'href' in date_link.attrib:
                            # Extract date from href which is in format /boxes/TEAM/TEAM202304160.shtml
                            href = date_link.attrib.get('href', '')
                            date_match = re.search(r'(\d{4})(\d{2})(\d{2})', href)
                            if date_match:
                                year, month, day = date_match.groups()
                                formatted_date = f"{year}-{month}-{day}"
                                row_data[data_stat] = formatted_date
                            else:
                                # If couldn't extract from href but link exists, use link text with year
                                link_text = date_link.text.clean()
                                if link_text and link_text.lower() != 'none':
                                    row_data[data_stat] = f"{year}-{link_text}"
                                else:
                                    # Use placeholder with year from function argument
                                    row_data[data_stat] = f"{year}-01-01"
                                    logger.warning(f"Using placeholder date for game in {year}")
                        else:
                            # If no link at all, use cell text or placeholder
                            cell_text = cell.text.clean()
                            if cell_text and cell_text.lower() != 'none':
                                row_data[data_stat] = f"{year}-{cell_text}"
                            else:
                                # Use placeholder date with year
                                row_data[data_stat] = f"{year}-01-01"
                                logger.warning(f"Using placeholder date for game in {year}")
                    # Special handling for team_ID and opp_ID fields
                    elif data_stat in ['team_ID', 'opp_ID']:
                        # Try to get the team code from the link text first
                        team_link = cell.css_first('a')
                        if team_link:
                            team_text = team_link.text.clean()
                            if team_text:  # If link text exists, use it
                                row_data[data_stat] = team_text
                            elif 'href' in team_link.attrib:  # Otherwise extract from href
                                href = team_link.attrib.get('href', '')
                                team_match = re.search(r'/teams/([A-Z]+)/', href)
                                if team_match:
                                    row_data[data_stat] = team_match.group(1)
                                else:
                                    row_data[data_stat] = None
                        else:
                            # If no link, try cell text
                            text = cell.text.clean()
                            row_data[data_stat] = text if text and text.lower() != 'none' else None
                    # Special handling for team_homeORaway field - represents home/away games
                    elif data_stat == 'team_homeORaway':
                        # '@' means away game, empty/None means home game
                        text = cell.text.clean()
                        if text == '@':
                            row_data[data_stat] = '@'  # Away game
                        else:
                            row_data[data_stat] = None  # Home game
                    else:
                        # For all other cells, just extract the text
                        row_data[data_stat] = cell.text.clean()
                        
                data.append(row_data)
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Log how many games were found
            num_games = len(df)
            logger.info(f"Found data for {num_games} games for {player_id} in {year}")
            
            if num_games == 0:
                logger.warning(f"No game data found for {player_id} in {year}")
                return None, player_name
            
            return df, player_name
            
        except Exception as e:
            logger.error(f"Error scraping {player_id} year {year}: {str(e)}")
            attempts += 1
            time.sleep(retry_delay)
    
    logger.error(f"Failed to scrape {player_id} year {year} after {retry_limit} attempts")
    return None, None


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