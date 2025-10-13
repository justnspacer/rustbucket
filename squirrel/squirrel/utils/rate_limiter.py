"""
Rate limiting utilities for squirrel service.
"""
import time
from collections import deque
from typing import Optional
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Token bucket rate limiter implementation.
    Limits the number of calls within a time period.
    """
    
    def __init__(self, max_calls: int, period: int):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self._lock = False
    
    def _cleanup_old_calls(self):
        """Remove calls outside the current time window."""
        current_time = time.time()
        cutoff_time = current_time - self.period
        
        while self.calls and self.calls[0] < cutoff_time:
            self.calls.popleft()
    
    def can_proceed(self) -> bool:
        """Check if a call can proceed without blocking."""
        self._cleanup_old_calls()
        return len(self.calls) < self.max_calls
    
    def wait_if_needed(self) -> float:
        """
        Wait if rate limit is exceeded.
        Returns the time waited in seconds.
        """
        self._cleanup_old_calls()
        
        if len(self.calls) < self.max_calls:
            self.calls.append(time.time())
            return 0.0
        
        # Calculate wait time
        oldest_call = self.calls[0]
        wait_time = (oldest_call + self.period) - time.time()
        
        if wait_time > 0:
            logger.debug(f"Rate limit reached, waiting {wait_time:.2f}s")
            time.sleep(wait_time)
            self._cleanup_old_calls()
        
        self.calls.append(time.time())
        return max(0, wait_time)
    
    def __call__(self, func):
        """Decorator to apply rate limiting to a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper
    
    def reset(self):
        """Reset the rate limiter."""
        self.calls.clear()
        logger.debug("Rate limiter reset")
    
    def get_stats(self) -> dict:
        """Get current rate limiter statistics."""
        self._cleanup_old_calls()
        return {
            'current_calls': len(self.calls),
            'max_calls': self.max_calls,
            'period': self.period,
            'calls_remaining': self.max_calls - len(self.calls),
            'percentage_used': (len(self.calls) / self.max_calls) * 100
        }


class AdaptiveRateLimiter(RateLimiter):
    """
    Adaptive rate limiter that adjusts based on success/failure rates.
    Backs off on errors and recovers on successes.
    """
    
    def __init__(self, max_calls: int, period: int, 
                 backoff_factor: float = 0.5, recovery_factor: float = 1.1):
        """
        Initialize adaptive rate limiter.
        
        Args:
            max_calls: Initial maximum calls
            period: Time period in seconds
            backoff_factor: Factor to reduce rate on errors (0.0-1.0)
            recovery_factor: Factor to increase rate on success (>1.0)
        """
        super().__init__(max_calls, period)
        self.initial_max_calls = max_calls
        self.backoff_factor = backoff_factor
        self.recovery_factor = recovery_factor
        self.consecutive_errors = 0
        self.consecutive_successes = 0
    
    def report_success(self):
        """Report a successful call."""
        self.consecutive_errors = 0
        self.consecutive_successes += 1
        
        # Gradually recover rate limit after multiple successes
        if self.consecutive_successes >= 5:
            old_limit = self.max_calls
            self.max_calls = min(
                int(self.max_calls * self.recovery_factor),
                self.initial_max_calls
            )
            if self.max_calls > old_limit:
                logger.info(f"Rate limit increased: {old_limit} -> {self.max_calls}")
            self.consecutive_successes = 0
    
    def report_error(self):
        """Report a failed call (triggers backoff)."""
        self.consecutive_successes = 0
        self.consecutive_errors += 1
        
        # Back off after consecutive errors
        if self.consecutive_errors >= 3:
            old_limit = self.max_calls
            self.max_calls = max(
                int(self.max_calls * self.backoff_factor),
                1  # Minimum 1 call
            )
            if self.max_calls < old_limit:
                logger.warning(f"Rate limit decreased due to errors: {old_limit} -> {self.max_calls}")
            self.consecutive_errors = 0


def rate_limit(max_calls: int, period: int):
    """
    Decorator factory for rate limiting functions.
    
    Args:
        max_calls: Maximum number of calls allowed
        period: Time period in seconds
    
    Example:
        @rate_limit(max_calls=10, period=60)
        def my_function():
            pass
    """
    limiter = RateLimiter(max_calls, period)
    return limiter
