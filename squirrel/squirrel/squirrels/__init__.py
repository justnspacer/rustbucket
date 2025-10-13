"""
Squirrels module.
"""
from .base_squirrel import BaseSquirrel, SquirrelException, RateLimitException, DataNotFoundException
from .foolsball_squirrel import FoolsballSquirrel
from .jobs_squirrel import JobsSquirrel

__all__ = [
    'BaseSquirrel',
    'SquirrelException',
    'RateLimitException',
    'DataNotFoundException',
    'FoolsballSquirrel',
    'JobsSquirrel',
]
