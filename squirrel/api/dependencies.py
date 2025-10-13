"""
Shared dependencies for route modules.
"""
from squirrel.squirrel_manager import SquirrelManager

def get_squirrel_manager() -> SquirrelManager:
    """Dependency to provide squirrel manager instance."""
    from run import squirrel_manager
    return squirrel_manager