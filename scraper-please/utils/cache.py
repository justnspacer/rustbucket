"""
Caching utilities for scraper service.
Supports both in-memory and Redis caching.
"""
import json
import time
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class CacheBackend:
    """Abstract cache backend interface."""
    
    def get(self, key: str) -> Optional[Any]:
        raise NotImplementedError
    
    def set(self, key: str, value: Any, ttl: int) -> bool:
        raise NotImplementedError
    
    def delete(self, key: str) -> bool:
        raise NotImplementedError
    
    def clear(self) -> bool:
        raise NotImplementedError


class InMemoryCache(CacheBackend):
    """Simple in-memory cache implementation."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        if time.time() > entry['expires_at']:
            del self._cache[key]
            return None
        
        logger.debug(f"Cache hit: {key}")
        return entry['value']
    
    def set(self, key: str, value: Any, ttl: int) -> bool:
        """Set value in cache with TTL (in seconds)."""
        try:
            self._cache[key] = {
                'value': value,
                'expires_at': time.time() + ttl,
                'created_at': time.time()
            }
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache delete: {key}")
            return True
        return False
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        self._cache.clear()
        logger.info("Cache cleared")
        return True
    
    def cleanup_expired(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time > entry['expires_at']
        ]
        for key in expired_keys:
            del self._cache[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")


class RedisCache(CacheBackend):
    """Redis cache implementation."""
    
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        try:
            import redis
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {host}:{port}")
        except ImportError:
            logger.warning("Redis package not installed. Falling back to in-memory cache.")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        try:
            value = self.redis_client.get(key)
            if value:
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int) -> bool:
        """Set value in Redis cache with TTL."""
        try:
            serialized = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis cache."""
        try:
            result = self.redis_client.delete(key)
            if result:
                logger.debug(f"Cache delete: {key}")
            return bool(result)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all keys in Redis database."""
        try:
            self.redis_client.flushdb()
            logger.info("Redis cache cleared")
            return True
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            return False


class Cache:
    """Unified cache interface that automatically selects backend."""
    
    def __init__(self, use_redis: bool = False, redis_host: str = 'localhost',
                 redis_port: int = 6379, redis_db: int = 0):
        self.backend: CacheBackend
        
        if use_redis:
            try:
                self.backend = RedisCache(redis_host, redis_port, redis_db)
                logger.info("Using Redis cache backend")
            except Exception as e:
                logger.warning(f"Failed to initialize Redis, using in-memory cache: {e}")
                self.backend = InMemoryCache()
        else:
            self.backend = InMemoryCache()
            logger.info("Using in-memory cache backend")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self.backend.get(key)
    
    def set(self, key: str, value: Any, ttl: int) -> bool:
        """Set value in cache with TTL (seconds)."""
        return self.backend.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        return self.backend.delete(key)
    
    def clear(self) -> bool:
        """Clear all cache."""
        return self.backend.clear()
    
    def get_or_set(self, key: str, func, ttl: int) -> Any:
        """Get from cache or execute function and cache result."""
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value
        
        value = func()
        self.set(key, value, ttl)
        return value
