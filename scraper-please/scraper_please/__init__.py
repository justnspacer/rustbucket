"""
Scraper-Please: A flexible web scraping framework.
"""
__version__ = '0.1.0'

# Make scrapers available at package level  
from .scrapers import FoolsballScraper, BaseScraper, ScraperException
from .scraper_manager import ScraperManager, ScraperType

__all__ = [
    'FoolsballScraper',
    'BaseScraper',
    'ScraperException',
    'ScraperManager',
    'ScraperType',
    '__version__'
]
