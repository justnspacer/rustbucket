"""
Scrapers module.
"""
from .base_scraper import BaseScraper, ScraperException, RateLimitException, DataNotFoundException
from .foolsball_scraper import FoolsballScraper
from .jobs_scraper import JobsScraper

__all__ = [
    'BaseScraper',
    'ScraperException',
    'RateLimitException',
    'DataNotFoundException',
    'FoolsballScraper',
    'JobsScraper',
]
