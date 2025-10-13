"""
API module for the squirrel service.
"""
from .routes import router
from .schemas import (
    ApiResponse,
    TeamResponse,
    PlayerResponse,
    GameScoreResponse,
    PlayerStatsResponse,
    SourceInfo,
    HealthResponse,
    ErrorResponse
)

__all__ = [
    'router',
    'ApiResponse',
    'TeamResponse',
    'PlayerResponse',
    'GameScoreResponse',
    'PlayerStatsResponse',
    'SourceInfo',
    'HealthResponse',
    'ErrorResponse'
]
