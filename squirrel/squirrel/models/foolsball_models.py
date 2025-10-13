"""
Data models for NFL football data.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TeamBase(BaseModel):
    """Base model for NFL team data."""
    id: str
    name: str
    abbreviation: str
    display_name: str
    location: str
    color: Optional[str] = None
    alternate_color: Optional[str] = None
    logo_url: Optional[str] = None


class Team(TeamBase):
    """Extended NFL team data."""
    conference: Optional[str] = None
    division: Optional[str] = None
    stadium: Optional[str] = None
    founded: Optional[int] = None
    record: Optional[Dict[str, int]] = None  # wins, losses, ties
    updated_at: datetime = Field(default_factory=datetime.now)


class PlayerBase(BaseModel):
    """Base model for NFL player data."""
    id: str
    name: str
    display_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    team_id: Optional[str] = None
    team_name: Optional[str] = None


class Player(PlayerBase):
    """Extended NFL player data with stats."""
    position: Optional[str] = None
    jersey_number: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[int] = None
    age: Optional[int] = None
    birth_date: Optional[str] = None
    college: Optional[str] = None
    experience: Optional[int] = None  # years in NFL
    headshot_url: Optional[str] = None
    status: Optional[str] = None  # active, injured, etc.
    updated_at: datetime = Field(default_factory=datetime.now)


class PlayerStats(BaseModel):
    """Player statistics model."""
    player_id: str
    player_name: str
    season: int
    week: Optional[int] = None
    stats: Dict[str, Any]  # Flexible stats structure
    updated_at: datetime = Field(default_factory=datetime.now)


class GameScore(BaseModel):
    """Live game score model."""
    game_id: str
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    quarter: Optional[str] = None
    time_remaining: Optional[str] = None
    status: str  # scheduled, in-progress, final
    updated_at: datetime = Field(default_factory=datetime.now)


class SquirrelResponse(BaseModel):
    """Standard response wrapper for squirrel results."""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    cached: bool = False
    timestamp: datetime = Field(default_factory=datetime.now)
    source: Optional[str] = None
