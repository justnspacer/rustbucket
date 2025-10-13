"""
Shared dependencies for route modules.
"""
from scraper_please.scraper_manager import ScraperManager

def get_scraper_manager() -> ScraperManager:
    """Dependency to provide scraper manager instance."""
    from run import scraper_manager
    return scraper_manager