#!/usr/bin/env python3
"""
High-Performance MLB Pitcher Game Logs Scraper
Uses async I/O, smart rate limiting, and optimized parsing for maximum speed
"""

import asyncio
import time
import random
import pandas as pd
import os
import aiohttp
from bs4 import BeautifulSoup, SoupStrainer
import logging
from pathlib import Path
from asyncio_throttle import Throttler
import aiolimiter
import signal
from functools import partial
import ujson as json
from io import StringIO
import backoff
from typing import List, Dict, Any, Optional, Tuple, Set
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Cache directory for saving responses
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Shared state for progress reporting
class ScraperState:
    def __init__(self, total_jobs):
        self.total_jobs = total_jobs
        self.completed = 0
        self.successful = 0
        self.start_time = time.time()
        self.last_update_time = time.time()
        self.failed_jobs = set()
        
    def update(self, success=False, pitcher_id=None, season=None):
        self.completed += 1
        if success:
            self.successful += 1
        else:
            if pitcher_id and season:
                self.failed_jobs.add((pitcher_id, season))
        
        # Update console progress only every 0.5 seconds to reduce overhead
        current_time = time.time()
        if current_time - self.last_update_time > 0.5:
            self._print_progress()
            self.last_update_time = current_time
    
    def _print_progress(self):
        percent = (self.completed / self.total_jobs) * 100
        elapsed = time.time() - self.start_time
        rate = self.completed / elapsed if elapsed > 0 else 0
        eta = (self.total_jobs - self.completed) / rate if rate > 0 else 0
        
        sys.stdout.write(f"\r📊 Progress: {self.completed}/{self.total_jobs} ({percent:.1f}%) | "
                        f"Success: {self.successful} | "
                        f"Rate: {rate:.1f} req/s | "
                        f"ETA: {eta:.1f}s ")
        sys.stdout.flush()

    def finalize(self):
        elapsed = time.time() - self.start_time
        sys.stdout.write("\n")  # Move to a new line
        logger.info(f"✅ Completed {self.completed}/{self.total_jobs} jobs in {elapsed:.2f}s")
        logger.info(f"✅ Success rate: {(self.successful/self.total_jobs)*100:.1f}%")
        return self.failed_jobs

# Optimize rate limiting with a combination of throttling and limiting
async def fetch_with_retries(session, url, pitcher_id, season, rate_limiter, cache_file):
    """Fetch URL with retry logic and rate limiting"""
    # Check cache first
    if cache_file.exists():
        try:
            return json.loads(cache_file.read_text())
        except (json.JSONDecodeError, OSError):
            # Invalid cache, continue to fetch
            pass
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=60
    )
    async def _fetch():
        # Apply rate limiting
        async with rate_limiter:
            await asyncio.sleep(random.uniform(0.1, 0.5))  # Small jitter
            
            try:
                async with session.get(url, timeout=15) as response:
                    if response.status == 404:
                        logger.warning(f"⚠️ 404 Error: No game logs for {pitcher_id} in {season}")
                        return None
                    
                    response.raise_for_status()
                    text = await response.text()
                    
                    # Cache the response
                    cache_file.write_text(json.dumps({
                        "status": response.status,
                        "url": url,
                        "text": text
                    }))
                    
                    return {
                        "status": response.status,
                        "url": url,
                        "text": text
                    }
            except aiohttp.ClientResponseError as e:
                if e.status == 429:  # Too Many Requests
                    logger.warning(f"Rate limited on {url}, backing off")
                    await asyncio.sleep(10)  # Long backoff
                raise
    
    return await _fetch()

async def parse_player_data(response_data, pitcher_id, season) -> Optional[pd.DataFrame]:
    """Parse HTML and extract game log table - optimized for speed"""
    if not response_data:
        return None
    
    try:
        # Use SoupStrainer to parse only the table section
        table_strainer = SoupStrainer("table", id="pitching_gamelogs")
        soup = BeautifulSoup(response_data["text"], "lxml", parse_only=table_strainer)
        
        # Find game log table
        table = soup.find("table", {"id": "pitching_gamelogs"})
        if not table:
            logger.warning(f"⚠️ No data table found for {pitcher_id} in {season}")
            return None
        
        # Convert to pandas dataframe using StringIO for better performance
        df = pd.read_html(StringIO(str(table)))[0]
        
        # Add metadata
        df["Pitcher_ID"] = pitcher_id
        df["Season"] = season
        
        # Clean up DataFrame (handling multilevel columns if present)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [' '.join(col).strip() for col in df.columns.values]
        
        # Remove rows that are section headers or totals
        df = df[~df.iloc[:, 0].str.contains('Rank', na=False)]
        
        return df
    
    except Exception as e:
        logger.error(f"⚠️ Error processing data for {pitcher_id} in {season}: {e}")
        return None

async def scrape_pitcher_logs(session, pitcher_id, season, rate_limiter, state):
    """Scrape game logs for a pitcher in a specific season using async requests"""
    url = f"https://www.baseball-reference.com/players/gl.fcgi?id={pitcher_id}&t=p&year={season}"
    
    # Create cache path
    cache_file = CACHE_DIR / f"{pitcher_id}_{season}.json"
    
    try:
        # Fetch data with rate limiting and retries
        response_data = await fetch_with_retries(
            session, url, pitcher_id, season, rate_limiter, cache_file
        )
        
        # Parse response data
        df = await parse_player_data(response_data, pitcher_id, season)
        
        # Update state tracker
        state.update(success=df is not None, pitcher_id=pitcher_id, season=season)
        
        return df
    except Exception as e:
        logger.error(f"Error fetching {pitcher_id} {season}: {str(e)}")
        state.update(success=False, pitcher_id=pitcher_id, season=season)
        return None

async def process_batch(batch, rate_limiter, state, dfs, session):
    """Process a batch of pitcher/season pairs concurrently"""
    tasks = []
    for pitcher_id, season in batch:
        task = asyncio.create_task(
            scrape_pitcher_logs(session, pitcher_id, season, rate_limiter, state)
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results, filtering out exceptions and None values
    for result in results:
        if isinstance(result, Exception):
            logger.error(f"Task exception: {str(result)}")
        elif result is not None and not result.empty:
            dfs.append(result)
    
    # Allow some time between batches to avoid overwhelming the server
    await asyncio.sleep(0.5)

async def scrape_all_pitchers_async(pitchers, seasons, output_file="MLB_Pitcher_Game_Logs.csv", 
                                   concurrent_requests=15, requests_per_second=5, 
                                   batch_size=20, retries=3):
    """
    Scrape multiple pitchers over multiple seasons using async processing
    
    Args:
        pitchers (list): List of pitcher IDs to scrape
        seasons (list): List of seasons to scrape
        output_file (str): Output file path
        concurrent_requests (int): Maximum number of concurrent connections
        requests_per_second (int): Rate limit for requests per second
        batch_size (int): Number of requests to process in each batch
        retries (int): Number of retries for failed requests
    """
    # Create all pitcher/season combinations
    job_pairs = [(pitcher, season) for pitcher in pitchers for season in seasons]
    total_jobs = len(job_pairs)
    
    # Initialize state tracker
    state = ScraperState(total_jobs)
    logger.info(f"Starting async scraper with {concurrent_requests} concurrent connections")
    logger.info(f"Rate limit: {requests_per_second} requests/second")
    
    # Collected dataframes
    dfs = []
    
    # Configure rate limiters
    throttler = Throttler(rate_limit=requests_per_second)
    
    # Custom headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    # Create connection pool with limits
    conn = aiohttp.TCPConnector(limit=concurrent_requests)
    timeout = aiohttp.ClientTimeout(total=60)
    
    # Process in batches
    async with aiohttp.ClientSession(connector=conn, timeout=timeout, headers=headers) as session:
        for i in range(0, len(job_pairs), batch_size):
            batch = job_pairs[i:i+batch_size]
            await process_batch(batch, throttler, state, dfs, session)
    
    # Print final stats
    failed_jobs = state.finalize()
    
    # Handle retries if specified
    if retries > 0 and failed_jobs:
        logger.info(f"Retrying {len(failed_jobs)} failed jobs (retry {4-retries}/3)")
        # Recursively retry with one fewer retry count
        retry_pitchers = [job[0] for job in failed_jobs]
        retry_seasons = [job[1] for job in failed_jobs]
        await scrape_all_pitchers_async(
            retry_pitchers, retry_seasons, 
            output_file=None,  # Don't save interim results
            concurrent_requests=concurrent_requests, 
            requests_per_second=requests_per_second//2,  # Lower rate for retries
            batch_size=batch_size,
            retries=retries-1
        )
    
    # Combine and save results
    if dfs and output_file:
        try:
            # Optimize concatenation with pandas
            final_df = pd.concat(dfs, ignore_index=True, copy=False)
            
            # Save to CSV efficiently
            final_df.to_csv(output_file, index=False)
            logger.info(f"✅ Data saved to {output_file} with {len(final_df)} rows")
            return final_df
        except Exception as e:
            logger.error(f"❌ Error saving data: {e}")
    elif not dfs:
        logger.warning("❌ No data was collected")
    
    return dfs

def main():
    """Main function to run the scraper"""
    # Handle graceful shutdown
    def signal_handler(sig, frame, loop):
        logger.info("Received shutdown signal, cleaning up...")
        for task in asyncio.all_tasks(loop):
            task.cancel()
        logger.info("Tasks canceled, shutting down...")
        loop.stop()
        sys.exit(0)
    
    # Load pitcher IDs
    try:
        pitchers_file = "Starting_Pitchers_IDs.csv"
        if not os.path.exists(pitchers_file):
            logger.error(f"Pitcher IDs file not found: {pitchers_file}")
            return
            
        pitchers_df = pd.read_csv(pitchers_file)
        pitchers = pitchers_df["Pitcher_ID"].tolist()
        logger.info(f"Loaded {len(pitchers)} pitchers from {pitchers_file}")
        
        # List of seasons to scrape
        seasons = [2020, 2021, 2022, 2023, 2024]
        
        # Get or create the event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Set up signal handlers for graceful shutdown
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: signal_handler(sig, None, loop))
        
        # Run the async scraper
        result = loop.run_until_complete(
            scrape_all_pitchers_async(
                pitchers=pitchers,
                seasons=seasons,
                concurrent_requests=20,       # Concurrent connections
                requests_per_second=10,       # Rate limit
                batch_size=30,                # Process in batches
                retries=3                     # Auto-retry failed jobs
            )
        )
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in main function: {e}")
        return None

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed = time.time() - start_time
    logger.info(f"🚀 Scraping complete in {elapsed:.2f} seconds") 