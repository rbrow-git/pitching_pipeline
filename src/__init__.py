"""
Baseball Reference Pitching Pipeline

A package for scraping and analyzing baseball pitching data from Baseball Reference.
"""

# Make core modules easily importable
from src.core import (
    scrape_player, scrape_year, scrape_and_store,
    initialize_database, get_players_in_database, update_player_in_database,
    load_player_ids, filter_players
)

__version__ = "0.1.0"
