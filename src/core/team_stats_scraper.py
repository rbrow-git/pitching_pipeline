#!/usr/bin/env python3
"""
Module for scraping baseball-reference.com team batting statistics
"""

import pandas as pd
import logging
from scrapling import StealthyFetcher
import re
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_team_stats(year=None, retry_limit=3):
    """
    Scrape team batting statistics for a specific year
    
    Args:
        year (int): Year to scrape, defaults to current year
        retry_limit (int): Number of retry attempts
        
    Returns:
        DataFrame: DataFrame containing team batting stats
    """
    # Use current year if not specified
    if not year:
        year = datetime.now().year
        
    logger.info(f"Scraping team batting stats for {year}")
    
    # URL for Baseball Reference Team Batting Stats
    url = f"https://www.baseball-reference.com/leagues/majors/{year}-standard-batting.shtml"
    
    # Initialize the fetcher
    fetcher = StealthyFetcher(delay=(2, 5), timeout=10)
    
    attempts = 0
    while attempts < retry_limit:
        attempts += 1
        logger.debug(f"Fetching team stats for {year} (attempt {attempts})")
        
        # Fetch with a retry
        response = fetcher.fetch(url)
        
        if not response:
            logger.warning(f"Failed to fetch {url} (attempt {attempts}/{retry_limit})")
            continue  # Try again
    
        # Look for the team batting stats table
        table_match = re.search(r'(<table[^>]*?id="teams_standard_batting"[^>]*?>.*?</table>)', response, re.DOTALL)
        
        if not table_match:
            logger.warning(f"Team batting stats table not found for {year}")
            return None
            
        table_html = table_match.group(1)
        
        try:
            # Use pandas to parse the HTML table
            dfs = pd.read_html(table_html)
            
            if not dfs or len(dfs) == 0:
                logger.warning(f"No data found in team batting stats table for {year}")
                return None
                
            df = dfs[0]
            
            # Clean up the DataFrame
            df = process_team_stats_df(df, year)
            
            if df is not None and not df.empty:
                logger.info(f"Successfully scraped team batting stats for {year}: {len(df)} teams")
                return df
            
        except Exception as e:
            logger.error(f"Error processing team stats for {year}: {str(e)}")
            continue  # Try again
    
    logger.error(f"Failed to scrape team stats for {year} after {retry_limit} attempts")
    return None
    
def process_team_stats_df(df, year):
    """
    Process the raw team stats dataframe
    
    Args:
        df (DataFrame): Raw team stats dataframe
        year (int): Year being scraped
        
    Returns:
        DataFrame: Processed dataframe with cleaned columns
    """
    # Skip if empty
    if df.empty:
        return df
        
    # Handle multi-index columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(1)
    
    # Rename team column to be consistent
    if 'Tm' in df.columns:
        df = df.rename(columns={'Tm': 'Team'})
    
    # Add year column
    df['year'] = year
    
    # Keep only relevant columns
    columns_to_keep = [
        'Team', 
        'year',
        'R/G',  # Runs per game 
        'G',    # Games
        'PA',   # Plate appearances
        'AB',   # At bats
        'R',    # Runs
        'H',    # Hits
        '2B',   # Doubles
        '3B',   # Triples
        'HR',   # Home runs
        'RBI',  # RBIs
        'SB',   # Stolen bases
        'CS',   # Caught stealing
        'BB',   # Walks
        'SO',   # Strikeouts
        'BA',   # Batting average
        'OBP',  # On-base percentage
        'SLG',  # Slugging
        'OPS',  # On-base plus slugging
        'OPS+', # OPS+
        'TB',   # Total bases
        'GDP',  # Grounded into double play
        'HBP',  # Hit by pitch
        'SH',   # Sacrifice hits
        'SF',   # Sacrifice flies
        'IBB'   # Intentional walks
    ]
    
    # Only keep columns that exist in the dataframe
    cols_to_use = [col for col in columns_to_keep if col in df.columns]
    df = df[cols_to_use]
    
    # Remove rows with missing team names or with "League Average" or "Total"
    df = df[df['Team'].notna()]
    df = df[~df['Team'].str.contains('League Average|Total', na=False)]
    
    # Convert numeric columns
    for col in df.columns:
        if col not in ['Team', 'year']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def save_team_stats(df, output_file="team_stats.csv"):
    """
    Save team stats to a CSV file
    
    Args:
        df (DataFrame): Team stats dataframe
        output_file (str): Output file path
        
    Returns:
        bool: Success or failure
    """
    if df is None or df.empty:
        logger.warning("No data to save")
        return False
        
    try:
        df.to_csv(output_file, index=False)
        logger.info(f"Team stats saved to {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving team stats: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    team_stats = scrape_team_stats()
    if team_stats is not None:
        save_team_stats(team_stats, "MLB_Team_Stats.csv")
