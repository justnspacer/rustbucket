"""
Scraper-Please: A flexible web scraping framework.
"""
__version__ = '0.1.0'

# Make scrapers available at package level  
from .scrapers import FoolsballScraper, BaseScraper

__all__ = ['FoolsballScraper', 'BaseScraper']
