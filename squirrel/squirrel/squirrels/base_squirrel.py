"""
Base squirrel class with common functionality for all squirrels.
Provides caching, rate limiting, error handling, and retry logic.
"""
import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List, Callable
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..utils.cache import Cache
from ..utils.rate_limiter import RateLimiter, AdaptiveRateLimiter
from ..config import (
    USER_AGENT, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY,
    RATE_LIMIT_CALLS, RATE_LIMIT_PERIOD, USE_REDIS, REDIS_HOST,
    REDIS_PORT, REDIS_DB, CACHE_TTL_DEFAULT
)

logger = logging.getLogger(__name__)


class SquirrelException(Exception):
    """Base exception for squirrel errors."""
    pass


class RateLimitException(SquirrelException):
    """Raised when rate limit is exceeded."""
    pass


class DataNotFoundException(SquirrelException):
    """Raised when expected data is not found."""
    pass


class BaseSquirrel(ABC):
    """
    Base squirrel class with common functionality.
    All specific squirrels should inherit from this class.
    """
    
    def __init__(
        self,
        cache_enabled: bool = True,
        rate_limit_enabled: bool = True,
        adaptive_rate_limit: bool = False,
        max_calls: Optional[int] = None,
        period: Optional[int] = None
    ):
        """
        Initialize base squirrel.
        
        Args:
            cache_enabled: Enable caching
            rate_limit_enabled: Enable rate limiting
            adaptive_rate_limit: Use adaptive rate limiter
            max_calls: Maximum calls per period (overrides config)
            period: Time period for rate limiting (overrides config)
        """
        self.cache_enabled = cache_enabled
        self.rate_limit_enabled = rate_limit_enabled
        
        # Initialize cache
        if self.cache_enabled:
            self.cache = Cache(
                use_redis=USE_REDIS,
                redis_host=REDIS_HOST,
                redis_port=REDIS_PORT,
                redis_db=REDIS_DB
            )
            logger.info(f"{self.__class__.__name__}: Cache initialized")
        else:
            self.cache = None
        
        # Initialize rate limiter
        if self.rate_limit_enabled:
            calls = max_calls or RATE_LIMIT_CALLS
            period_seconds = period or RATE_LIMIT_PERIOD
            
            if adaptive_rate_limit:
                self.rate_limiter = AdaptiveRateLimiter(calls, period_seconds)
                logger.info(f"{self.__class__.__name__}: Adaptive rate limiter initialized")
            else:
                self.rate_limiter = RateLimiter(calls, period_seconds)
                logger.info(f"{self.__class__.__name__}: Rate limiter initialized")
        else:
            self.rate_limiter = None
        
        # Initialize HTTP session with retry strategy
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        return session
    
    def _get_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """
        Generate a cache key from arguments.
        
        Args:
            prefix: Cache key prefix
            *args: Positional arguments
            **kwargs: Keyword arguments
        
        Returns:
            Cache key string
        """
        key_parts = [prefix]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        return ":".join(key_parts)
    
    def _make_request(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> requests.Response:
        """
        Make an HTTP request with rate limiting and error handling.
        
        Args:
            url: URL to request
            method: HTTP method (GET, POST, etc.)
            headers: Additional headers
            params: Query parameters
            data: Request body data
            timeout: Request timeout
        
        Returns:
            Response object
        
        Raises:
            SquirrelException: On request failure
        """
        # Apply rate limiting
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()
        
        # Prepare request
        request_kwargs = {
            'timeout': timeout or REQUEST_TIMEOUT,
            'params': params,
        }
        
        if headers:
            request_kwargs['headers'] = headers
        
        if data:
            request_kwargs['json'] = data
        
        try:
            logger.debug(f"Making {method} request to {url}")
            response = self.session.request(method, url, **request_kwargs)
            response.raise_for_status()
            
            # Report success for adaptive rate limiter
            if isinstance(self.rate_limiter, AdaptiveRateLimiter):
                self.rate_limiter.report_success()
            
            return response
            
        except requests.exceptions.HTTPError as e:
            # Report error for adaptive rate limiter
            if isinstance(self.rate_limiter, AdaptiveRateLimiter):
                self.rate_limiter.report_error()
            
            if e.response.status_code == 429:
                logger.warning(f"Rate limit exceeded for {url}")
                raise RateLimitException(f"Rate limit exceeded: {url}")
            else:
                logger.error(f"HTTP error for {url}: {e}")
                raise SquirrelException(f"HTTP error: {e}")
        
        except requests.exceptions.RequestException as e:
            if isinstance(self.rate_limiter, AdaptiveRateLimiter):
                self.rate_limiter.report_error()
            
            logger.error(f"Request failed for {url}: {e}")
            raise SquirrelException(f"Request failed: {e}")
    
    def fetch_with_cache(
        self,
        cache_key: str,
        fetch_func: Callable,
        ttl: Optional[int] = None
    ) -> Any:
        """
        Fetch data with caching support.
        
        Args:
            cache_key: Cache key
            fetch_func: Function to fetch data if not cached
            ttl: Cache TTL in seconds
        
        Returns:
            Fetched or cached data
        """
        # Try cache first
        if self.cache:
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_data
        
        # Fetch fresh data
        logger.debug(f"Cache miss: {cache_key}")
        data = fetch_func()
        
        # Store in cache
        if self.cache and data is not None:
            cache_ttl = ttl or CACHE_TTL_DEFAULT
            self.cache.set(cache_key, data, cache_ttl)
            logger.debug(f"Cached data: {cache_key} (TTL: {cache_ttl}s)")
        
        return data
    
    def invalidate_cache(self, cache_key: Optional[str] = None):
        """
        Invalidate cache entries.
        
        Args:
            cache_key: Specific key to invalidate, or None to clear all
        """
        if not self.cache:
            return
        
        if cache_key:
            self.cache.delete(cache_key)
            logger.info(f"Cache invalidated: {cache_key}")
        else:
            self.cache.clear()
            logger.info("All cache cleared")
    
    @abstractmethod
    def scrape(self, *args, **kwargs) -> Any:
        """
        Main search method to be implemented by subclasses.
        
        Returns:
            Scraped data
        """
        pass
    
    def close(self):
        """Close the squirrel and cleanup resources."""
        if self.session:
            self.session.close()
            logger.info(f"{self.__class__.__name__}: Session closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
