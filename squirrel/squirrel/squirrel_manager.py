"""
Centralized squirrel manager for handling multiple squirrel instances.
Provides source switching, unified caching, and lifecycle management.
"""
import logging
from typing import Dict, Optional, Any, List
from enum import Enum

from .squirrels import BaseSquirrel, FoolsballSquirrel, JobsSquirrel
from .config import DEFAULT_NFL_SOURCE, NFL_DATA_SOURCES

logger = logging.getLogger(__name__)


class SquirrelType(str, Enum):
    """Available squirrel types."""
    FOOLSBALL = "foolsball"
    JOBS = "jobs"


class SquirrelManager:
    """
    Manages multiple squirrel instances with source switching capabilities.
    Provides a unified interface for all search operations.
    """
    
    def __init__(
        self,
        cache_enabled: bool = True,
        rate_limit_enabled: bool = True
    ):
        """
        Initialize squirrel manager.
        
        Args:
            cache_enabled: Enable caching for all squirrels
            rate_limit_enabled: Enable rate limiting for all squirrels
        """
        self.cache_enabled = cache_enabled
        self.rate_limit_enabled = rate_limit_enabled
        
        # Active squirrel instances
        self._squirrels: Dict[str, BaseSquirrel] = {}
        
        # Current active sources per squirrel type
        self._active_sources: Dict[SquirrelType, str] = {
            SquirrelType.FOOLSBALL: DEFAULT_NFL_SOURCE
        }
        
        logger.info("SquirrelManager initialized")
    
    def get_squirrel(
        self,
        squirrel_type: SquirrelType,
        source: Optional[str] = None
    ) -> BaseSquirrel:
        """
        Get or create a squirrel instance.
        
        Args:
            squirrel_type: Type of squirrel to get
            source: Data source (optional, uses active source if not provided)
        
        Returns:
            Squirrel instance
        
        Raises:
            ValueError: If squirrel type is not supported
        """
        # Determine source
        if source is None:
            source = self._active_sources.get(squirrel_type)
        
        # Create squirrel key
        squirrel_key = f"{squirrel_type}:{source}"
        
        # Return existing squirrel or create new one
        if squirrel_key not in self._squirrels:
            logger.info(f"Creating new squirrel: {squirrel_key}")
            
            if squirrel_type == SquirrelType.FOOLSBALL:
                self._squirrels[squirrel_key] = FoolsballSquirrel(
                    source=source,
                    cache_enabled=self.cache_enabled,
                    rate_limit_enabled=self.rate_limit_enabled
                )
            elif squirrel_type == SquirrelType.JOBS:
                self._squirrels[squirrel_key] = JobsSquirrel(
                    cache_enabled=self.cache_enabled,
                    rate_limit_enabled=self.rate_limit_enabled
                )
            else:
                raise ValueError(f"Unsupported squirrel type: {squirrel_type}")
        
        return self._squirrels[squirrel_key]
    
    def switch_source(self, squirrel_type: SquirrelType, source: str) -> None:
        """
        Switch the active data source for a squirrel type.
        
        Args:
            squirrel_type: Type of squirrel
            source: New data source
        
        Raises:
            ValueError: If source is not valid for the squirrel type
        """
        # Validate source
        if squirrel_type == SquirrelType.FOOLSBALL:
            if source not in NFL_DATA_SOURCES:
                raise ValueError(
                    f"Invalid source '{source}' for {squirrel_type}. "
                    f"Valid sources: {list(NFL_DATA_SOURCES.keys())}"
                )
        
        self._active_sources[squirrel_type] = source
        logger.info(f"Switched {squirrel_type} source to: {source}")
    
    def get_active_source(self, squirrel_type: SquirrelType) -> str:
        """
        Get the current active source for a squirrel type.
        
        Args:
            squirrel_type: Type of squirrel
        
        Returns:
            Active source name
        """
        return self._active_sources.get(squirrel_type, "unknown")
    
    def get_available_sources(self, squirrel_type: SquirrelType) -> List[str]:
        """
        Get list of available data sources for a squirrel type.
        
        Args:
            squirrel_type: Type of squirrel
        
        Returns:
            List of available source names
        """
        if squirrel_type == SquirrelType.FOOLSBALL:
            return list(NFL_DATA_SOURCES.keys())
        return []
    
    def invalidate_cache(
        self,
        squirrel_type: Optional[SquirrelType] = None,
        source: Optional[str] = None,
        cache_key: Optional[str] = None
    ) -> None:
        """
        Invalidate cache for specific squirrel(s).
        
        Args:
            squirrel_type: Specific squirrel type (None for all)
            source: Specific source (None for all sources of type)
            cache_key: Specific cache key to invalidate
        """
        if squirrel_type and source:
            # Invalidate specific squirrel
            squirrel_key = f"{squirrel_type}:{source}"
            if squirrel_key in self._squirrels:
                self._squirrels[squirrel_key].invalidate_cache(cache_key)
                logger.info(f"Cache invalidated for {squirrel_key}")
        
        elif squirrel_type:
            # Invalidate all squirrels of this type
            for key, squirrel in self._squirrels.items():
                if key.startswith(f"{squirrel_type}:"):
                    squirrel.invalidate_cache(cache_key)
            logger.info(f"Cache invalidated for all {squirrel_type} squirrels")
        
        else:
            # Invalidate all squirrels
            for squirrel in self._squirrels.values():
                squirrel.invalidate_cache(cache_key)
            logger.info("Cache invalidated for all squirrels")
    
    def get_squirrel_stats(self) -> Dict[str, Any]:
        """
        Get statistics for all active squirrels.
        
        Returns:
            Dictionary with squirrel statistics
        """
        stats = {
            "active_squirrels": len(self._squirrels),
            "active_sources": dict(self._active_sources),
            "squirrels": {}
        }
        
        for key, squirrel in self._squirrels.items():
            squirrel_stats = {
                "type": key.split(":")[0],
                "source": key.split(":")[1] if ":" in key else "unknown",
                "cache_enabled": squirrel.cache_enabled,
                "rate_limit_enabled": squirrel.rate_limit_enabled,
            }
            
            # Add rate limiter stats if available
            if squirrel.rate_limiter:
                squirrel_stats["rate_limiter"] = squirrel.rate_limiter.get_stats()
            
            stats["squirrels"][key] = squirrel_stats
        
        return stats
    
    def close_all(self) -> None:
        """Close all active squirrels and cleanup resources."""
        for key, squirrel in self._squirrels.items():
            try:
                squirrel.close()
                logger.info(f"Closed squirrel: {key}")
            except Exception as e:
                logger.error(f"Error closing squirrel {key}: {e}")
        
        self._squirrels.clear()
        logger.info("All squirrels closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_all()
