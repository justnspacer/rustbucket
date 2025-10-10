"""
API request and response schemas.
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# Request schemas
class SourceSwitchRequest(BaseModel):
    """Request to switch data source."""
    scraper_type: str = Field(..., description="Type of scraper (e.g., 'foolsball')")
    source: str = Field(..., description="New data source name (e.g., 'espn', 'nfl')")


class CacheInvalidationRequest(BaseModel):
    """Request to invalidate cache."""
    scraper_type: Optional[str] = Field(None, description="Scraper type to invalidate (all if not specified)")
    source: Optional[str] = Field(None, description="Specific source to invalidate")
    cache_key: Optional[str] = Field(None, description="Specific cache key to invalidate")


class PlayerStatsRequest(BaseModel):
    """Request for player statistics."""
    player_id: str = Field(..., description="Player ID")
    season: Optional[int] = Field(None, description="Season year (current year if not specified)")


# Response schemas
class ApiResponse(BaseModel):
    """Generic API response wrapper."""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[Any] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    cached: bool = Field(False, description="Whether data was served from cache")
    source: Optional[str] = Field(None, description="Data source used")


class TeamResponse(BaseModel):
    """Team data response."""
    id: str
    name: str
    abbreviation: str
    display_name: str
    location: str
    color: Optional[str] = None
    alternate_color: Optional[str] = None
    logo_url: Optional[str] = None
    conference: Optional[str] = None
    division: Optional[str] = None
    stadium: Optional[str] = None
    founded: Optional[int] = None
    record: Optional[Dict[str, int]] = None


class PlayerResponse(BaseModel):
    """Player data response."""
    id: str
    name: str
    display_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    team_id: Optional[str] = None
    team_name: Optional[str] = None
    position: Optional[str] = None
    jersey_number: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    age: Optional[int] = None
    birth_date: Optional[str] = None
    college: Optional[str] = None
    experience: Optional[int] = None
    headshot_url: Optional[str] = None
    status: Optional[str] = None


class GameScoreResponse(BaseModel):
    """Game score response."""
    game_id: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    quarter: Optional[str] = None
    time_remaining: Optional[str] = None
    status: str


class PlayerStatsResponse(BaseModel):
    """Player statistics response."""
    player_id: str
    player_name: str
    season: int
    week: Optional[int] = None
    stats: Dict[str, Any]


class SourceInfo(BaseModel):
    """Data source information."""
    scraper_type: str
    active_source: str
    available_sources: List[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str
    scraper_stats: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
