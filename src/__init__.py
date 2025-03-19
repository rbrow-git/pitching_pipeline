"""
Baseball Reference Pitching Pipeline

A package for scraping and analyzing baseball pitching data from Baseball Reference.
"""

# Make core modules easily importable
from src.core.gamelog_scraper import scrape_player, scrape_year
from src.core.scraper_manager import scrape_and_store, initialize_database
from src.core.player_utils import load_player_ids, filter_players

__version__ = "0.1.0"
