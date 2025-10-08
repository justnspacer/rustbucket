"""
Scrapers module.
"""
from .base_scraper import BaseScraper, ScraperException, RateLimitException, DataNotFoundException
from .foolsball_scraper import FoolsballScraper

__all__ = [
    'BaseScraper',
    'ScraperException',
    'RateLimitException',
    'DataNotFoundException',
    'FoolsballScraper',
]
