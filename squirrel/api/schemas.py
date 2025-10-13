"""
API request and response schemas.
"""
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# Request schemas
class SourceSwitchRequest(BaseModel):
    """Request to switch data source."""
    squirrel_type: str = Field(..., description="Type of squirrel (e.g., 'foolsball')")
    source: str = Field(..., description="New data source name (e.g., 'espn', 'nfl')")


class CacheInvalidationRequest(BaseModel):
    """Request to invalidate cache."""
    squirrel_type: Optional[str] = Field(None, description="Squirrel type to invalidate (all if not specified)")
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
    squirrel_type: str
    active_source: str
    available_sources: List[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str
    squirrel_stats: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


# Job squirrel schemas
class JobSearchRequest(BaseModel):
    """Request for job search."""
    keywords: str = Field(..., description="Search keywords (e.g., 'Python developer')")
    location: Optional[str] = Field(None, description="Job location (e.g., 'Chicago')")
    page: int = Field(1, ge=1, description="Page number")
    num_pages: int = Field(1, ge=1, le=10, description="Number of pages to fetch")
    country: str = Field("us", description="Country code")
    date_posted: str = Field("all", description="Date filter: all, today, 3days, week, month")
    employment_type: Optional[str] = Field(None, description="Employment type: fulltime, parttime, contractor, intern")
    remote_jobs_only: bool = Field(False, description="Filter for remote jobs only")


class JobFilterRequest(BaseModel):
    """Request for job filtering options."""
    remove_duplicates: bool = Field(True, description="Remove duplicate postings")
    check_red_flags: bool = Field(True, description="Check for suspicious terms")
    trusted_only: bool = Field(True, description="Only include trusted domains")
    validate_description: bool = Field(True, description="Validate description quality")


class ResumeMatchRequest(BaseModel):
    """Request for resume matching."""
    resume_text: str = Field(..., description="Resume text content")
    threshold: float = Field(0.2, ge=0.0, le=1.0, description="Minimum match score threshold")


class CoverLetterRequest(BaseModel):
    """Request for cover letter generation."""
    job_title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    job_description: str = Field(..., description="Job description")
    resume_summary: str = Field(..., description="Brief summary of candidate's experience")


class JobResponse(BaseModel):
    """Job posting response."""
    title: str
    company: str
    description: str
    url: str
    location: Optional[str] = None
    salary: Optional[str] = None
    date_posted: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    match_score: Optional[float] = None


class JobMatchResponse(BaseModel):
    """Job match response with score."""
    job: JobResponse
    match_score: float
    matched_keywords: List[str] = []


class CoverLetterResponse(BaseModel):
    """Cover letter response."""
    job_title: str
    company: str
    content: str
    generated_at: str
