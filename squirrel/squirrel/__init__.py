"""
Squirrel: A flexible web search framework.
"""
__version__ = '0.1.0'

# Make squirrels available at package level  
from .squirrels import FoolsballSquirrel, BaseSquirrel, SquirrelException
from .squirrel_manager import SquirrelManager, SquirrelType

__all__ = [
    'FoolsballSquirrel',
    'BaseSquirrel',
    'SquirrelException',
    'SquirrelManager',
    'SquirrelType',
    '__version__'
]
