"""
Centralized scraper manager for handling multiple scraper instances.
Provides source switching, unified caching, and lifecycle management.
"""
import logging
from typing import Dict, Optional, Any, List
from enum import Enum

from .scrapers import BaseScraper, FoolsballScraper, JobsScraper
from .config import DEFAULT_NFL_SOURCE, NFL_DATA_SOURCES

logger = logging.getLogger(__name__)


class ScraperType(str, Enum):
    """Available scraper types."""
    FOOLSBALL = "foolsball"
    JOBS = "jobs"


class ScraperManager:
    """
    Manages multiple scraper instances with source switching capabilities.
    Provides a unified interface for all scraping operations.
    """
    
    def __init__(
        self,
        cache_enabled: bool = True,
        rate_limit_enabled: bool = True
    ):
        """
        Initialize scraper manager.
        
        Args:
            cache_enabled: Enable caching for all scrapers
            rate_limit_enabled: Enable rate limiting for all scrapers
        """
        self.cache_enabled = cache_enabled
        self.rate_limit_enabled = rate_limit_enabled
        
        # Active scraper instances
        self._scrapers: Dict[str, BaseScraper] = {}
        
        # Current active sources per scraper type
        self._active_sources: Dict[ScraperType, str] = {
            ScraperType.FOOLSBALL: DEFAULT_NFL_SOURCE
        }
        
        logger.info("ScraperManager initialized")
    
    def get_scraper(
        self,
        scraper_type: ScraperType,
        source: Optional[str] = None
    ) -> BaseScraper:
        """
        Get or create a scraper instance.
        
        Args:
            scraper_type: Type of scraper to get
            source: Data source (optional, uses active source if not provided)
        
        Returns:
            Scraper instance
        
        Raises:
            ValueError: If scraper type is not supported
        """
        # Determine source
        if source is None:
            source = self._active_sources.get(scraper_type)
        
        # Create scraper key
        scraper_key = f"{scraper_type}:{source}"
        
        # Return existing scraper or create new one
        if scraper_key not in self._scrapers:
            logger.info(f"Creating new scraper: {scraper_key}")
            
            if scraper_type == ScraperType.FOOLSBALL:
                self._scrapers[scraper_key] = FoolsballScraper(
                    source=source,
                    cache_enabled=self.cache_enabled,
                    rate_limit_enabled=self.rate_limit_enabled
                )
            elif scraper_type == ScraperType.JOBS:
                self._scrapers[scraper_key] = JobsScraper(
                    cache_enabled=self.cache_enabled,
                    rate_limit_enabled=self.rate_limit_enabled
                )
            else:
                raise ValueError(f"Unsupported scraper type: {scraper_type}")
        
        return self._scrapers[scraper_key]
    
    def switch_source(self, scraper_type: ScraperType, source: str) -> None:
        """
        Switch the active data source for a scraper type.
        
        Args:
            scraper_type: Type of scraper
            source: New data source
        
        Raises:
            ValueError: If source is not valid for the scraper type
        """
        # Validate source
        if scraper_type == ScraperType.FOOLSBALL:
            if source not in NFL_DATA_SOURCES:
                raise ValueError(
                    f"Invalid source '{source}' for {scraper_type}. "
                    f"Valid sources: {list(NFL_DATA_SOURCES.keys())}"
                )
        
        self._active_sources[scraper_type] = source
        logger.info(f"Switched {scraper_type} source to: {source}")
    
    def get_active_source(self, scraper_type: ScraperType) -> str:
        """
        Get the current active source for a scraper type.
        
        Args:
            scraper_type: Type of scraper
        
        Returns:
            Active source name
        """
        return self._active_sources.get(scraper_type, "unknown")
    
    def get_available_sources(self, scraper_type: ScraperType) -> List[str]:
        """
        Get list of available data sources for a scraper type.
        
        Args:
            scraper_type: Type of scraper
        
        Returns:
            List of available source names
        """
        if scraper_type == ScraperType.FOOLSBALL:
            return list(NFL_DATA_SOURCES.keys())
        return []
    
    def invalidate_cache(
        self,
        scraper_type: Optional[ScraperType] = None,
        source: Optional[str] = None,
        cache_key: Optional[str] = None
    ) -> None:
        """
        Invalidate cache for specific scraper(s).
        
        Args:
            scraper_type: Specific scraper type (None for all)
            source: Specific source (None for all sources of type)
            cache_key: Specific cache key to invalidate
        """
        if scraper_type and source:
            # Invalidate specific scraper
            scraper_key = f"{scraper_type}:{source}"
            if scraper_key in self._scrapers:
                self._scrapers[scraper_key].invalidate_cache(cache_key)
                logger.info(f"Cache invalidated for {scraper_key}")
        
        elif scraper_type:
            # Invalidate all scrapers of this type
            for key, scraper in self._scrapers.items():
                if key.startswith(f"{scraper_type}:"):
                    scraper.invalidate_cache(cache_key)
            logger.info(f"Cache invalidated for all {scraper_type} scrapers")
        
        else:
            # Invalidate all scrapers
            for scraper in self._scrapers.values():
                scraper.invalidate_cache(cache_key)
            logger.info("Cache invalidated for all scrapers")
    
    def get_scraper_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all active scrapers.
        
        Returns:
            Dictionary with scraper statistics
        """
        stats = {
            "active_scrapers": len(self._scrapers),
            "active_sources": dict(self._active_sources),
            "scrapers": {}
        }
        
        for key, scraper in self._scrapers.items():
            scraper_stats = {
                "type": key.split(":")[0],
                "source": key.split(":")[1] if ":" in key else "unknown",
                "cache_enabled": scraper.cache_enabled,
                "rate_limit_enabled": scraper.rate_limit_enabled,
            }
            
            # Add rate limiter stats if available
            if scraper.rate_limiter:
                scraper_stats["rate_limiter"] = scraper.rate_limiter.get_stats()
            
            stats["scrapers"][key] = scraper_stats
        
        return stats
    
    def close_all(self) -> None:
        """Close all active scrapers and cleanup resources."""
        for key, scraper in self._scrapers.items():
            try:
                scraper.close()
                logger.info(f"Closed scraper: {key}")
            except Exception as e:
                logger.error(f"Error closing scraper {key}: {e}")
        
        self._scrapers.clear()
        logger.info("All scrapers closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_all()
