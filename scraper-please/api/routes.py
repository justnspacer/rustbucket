"""
API routes for the scraper service.
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends, status

from scraper_please.scraper_manager import ScraperManager, ScraperType
from scraper_please.scrapers import ScraperException, DataNotFoundException
from scraper_please.models.foolsball_models import Team, Player, GameScore, PlayerStats
from api.schemas import (
    ApiResponse, TeamResponse, PlayerResponse, GameScoreResponse,
    PlayerStatsResponse, SourceSwitchRequest, CacheInvalidationRequest,
    SourceInfo, PlayerStatsRequest, ErrorResponse
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


# Dependency to get scraper manager
def get_scraper_manager() -> ScraperManager:
    """Dependency to provide scraper manager instance."""
    # This will be injected by the FastAPI app
    from run import scraper_manager
    return scraper_manager


# Teams endpoints
@router.get(
    "/teams",
    response_model=ApiResponse,
    summary="Get all NFL teams",
    description="Fetches all NFL teams. Data is cached for 24 hours."
)
async def get_teams(
    source: Optional[str] = Query(None, description="Data source to use (espn, nfl)"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get all NFL teams."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        teams = scraper.get_teams()
        
        return ApiResponse(
            success=True,
            data=[team.dict() for team in teams],
            source=scraper.source,
            cached=False  # Could track this from cache
        )
    except ScraperException as e:
        logger.error(f"Error fetching teams: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get(
    "/teams/{team_id}",
    response_model=ApiResponse,
    summary="Get specific team",
    description="Fetches details for a specific NFL team."
)
async def get_team(
    team_id: str,
    source: Optional[str] = Query(None, description="Data source to use"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get specific team by ID."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        teams = scraper.get_teams()
        
        # Find the specific team
        team = next((t for t in teams if t.id == team_id), None)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
        
        return ApiResponse(
            success=True,
            data=team.dict(),
            source=scraper.source
        )
    except HTTPException:
        raise
    except ScraperException as e:
        logger.error(f"Error fetching team {team_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Players endpoints
@router.get(
    "/players",
    response_model=ApiResponse,
    summary="Get NFL players",
    description="Fetches NFL players, optionally filtered by team. Data is cached for 5 minutes."
)
async def get_players(
    team_id: Optional[str] = Query(None, description="Filter by team ID"),
    source: Optional[str] = Query(None, description="Data source to use"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get NFL players."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        players = scraper.get_players(team_id)
        
        return ApiResponse(
            success=True,
            data=[player.dict() for player in players],
            source=scraper.source
        )
    except ScraperException as e:
        logger.error(f"Error fetching players: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/players/{player_id}",
    response_model=ApiResponse,
    summary="Get specific player",
    description="Fetches detailed data for a specific NFL player."
)
async def get_player(
    player_id: str,
    source: Optional[str] = Query(None, description="Data source to use"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get specific player by ID."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        player = scraper.get_player(player_id)
        
        return ApiResponse(
            success=True,
            data=player.dict(),
            source=scraper.source
        )
    except DataNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ScraperException as e:
        logger.error(f"Error fetching player {player_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/players/{player_id}/stats",
    response_model=ApiResponse,
    summary="Get player statistics",
    description="Fetches statistics for a specific NFL player."
)
async def get_player_stats(
    player_id: str,
    season: Optional[int] = Query(None, description="Season year"),
    source: Optional[str] = Query(None, description="Data source to use"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get player statistics."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        stats = scraper.get_player_stats(player_id, season)
        
        return ApiResponse(
            success=True,
            data=stats.dict(),
            source=scraper.source
        )
    except DataNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ScraperException as e:
        logger.error(f"Error fetching stats for player {player_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Scores endpoints
@router.get(
    "/scores",
    response_model=ApiResponse,
    summary="Get live scores",
    description="Fetches live NFL game scores. Not cached - always returns fresh data."
)
async def get_scores(
    source: Optional[str] = Query(None, description="Data source to use"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get live game scores."""
    try:
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source)
        scores = scraper.get_live_scores()
        
        return ApiResponse(
            success=True,
            data=[score.dict() for score in scores],
            source=scraper.source,
            cached=False
        )
    except ScraperException as e:
        logger.error(f"Error fetching scores: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Source management endpoints
@router.get(
    "/sources",
    response_model=List[SourceInfo],
    summary="Get available data sources",
    description="Lists all available data sources for each scraper type."
)
async def get_sources(
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get available data sources."""
    sources = []
    for scraper_type in ScraperType:
        sources.append(SourceInfo(
            scraper_type=scraper_type.value,
            active_source=manager.get_active_source(scraper_type),
            available_sources=manager.get_available_sources(scraper_type)
        ))
    return sources


@router.post(
    "/sources/switch",
    response_model=ApiResponse,
    summary="Switch data source",
    description="Switches the active data source for a scraper type."
)
async def switch_source(
    request: SourceSwitchRequest,
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Switch data source."""
    try:
        scraper_type = ScraperType(request.scraper_type)
        manager.switch_source(scraper_type, request.source)
        
        return ApiResponse(
            success=True,
            data={
                "scraper_type": request.scraper_type,
                "new_source": request.source,
                "message": f"Switched {request.scraper_type} source to {request.source}"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Cache management endpoints
@router.post(
    "/cache/invalidate",
    response_model=ApiResponse,
    summary="Invalidate cache",
    description="Invalidates cache for specified scraper(s) or cache keys."
)
async def invalidate_cache(
    request: CacheInvalidationRequest,
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Invalidate cache."""
    try:
        scraper_type = ScraperType(request.scraper_type) if request.scraper_type else None
        manager.invalidate_cache(scraper_type, request.source, request.cache_key)
        
        message = "Cache invalidated"
        if request.cache_key:
            message += f" for key: {request.cache_key}"
        elif request.scraper_type:
            message += f" for {request.scraper_type}"
            if request.source:
                message += f":{request.source}"
        else:
            message += " for all scrapers"
        
        return ApiResponse(
            success=True,
            data={"message": message}
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete(
    "/cache",
    response_model=ApiResponse,
    summary="Clear all cache",
    description="Clears all cached data for all scrapers."
)
async def clear_cache(
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Clear all cache."""
    manager.invalidate_cache()
    return ApiResponse(
        success=True,
        data={"message": "All cache cleared"}
    )


# Stats and health endpoints
@router.get(
    "/stats",
    summary="Get scraper statistics",
    description="Returns statistics about active scrapers and their usage."
)
async def get_stats(
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """Get scraper statistics."""
    return manager.get_scraper_stats()
