import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends, status
from squirrel.squirrel_manager import SquirrelManager, SquirrelType
from squirrel.squirrels import SquirrelException, DataNotFoundException
from api.schemas import (ApiResponse)
from .dependencies import get_squirrel_manager

logger = logging.getLogger(__name__)
router = APIRouter()

# Teams endpoints
@router.get(
    "/teams",
    response_model=ApiResponse,
    summary="Get all NFL teams",
    description="Fetches all NFL teams. Data is cached for 24 hours."
)
async def get_teams(
    source: Optional[str] = Query(None, description="Data source to use (espn, nfl)"),
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get all NFL teams."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        teams = squirrel.get_teams()
        
        return ApiResponse(
            success=True,
            data=[team.dict() for team in teams],
            source=squirrel.source,
            cached=False  # Could track this from cache
        )
    except SquirrelException as e:
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get specific team by ID."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        teams = squirrel.get_teams()
        
        # Find the specific team
        team = next((t for t in teams if t.id == team_id), None)
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Team {team_id} not found")
        
        return ApiResponse(
            success=True,
            data=team.dict(),
            source=squirrel.source
        )
    except HTTPException:
        raise
    except SquirrelException as e:
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get NFL players."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        players = squirrel.get_players(team_id)
        
        return ApiResponse(
            success=True,
            data=[player.dict() for player in players],
            source=squirrel.source
        )
    except SquirrelException as e:
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get specific player by ID."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        player = squirrel.get_player(player_id)
        
        return ApiResponse(
            success=True,
            data=player.dict(),
            source=squirrel.source
        )
    except DataNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SquirrelException as e:
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get player statistics."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        stats = squirrel.get_player_stats(player_id, season)
        
        return ApiResponse(
            success=True,
            data=stats.dict(),
            source=squirrel.source
        )
    except DataNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SquirrelException as e:
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get live game scores."""
    try:
        squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source)
        scores = squirrel.get_live_scores()
        
        # Convert GameScore objects to dictionaries (compatible with both Pydantic v1 and v2)
        scores_data = []
        for score in scores:
            if hasattr(score, 'model_dump'):
                scores_data.append(score.model_dump())
            elif hasattr(score, 'dict'):
                scores_data.append(score.dict())
            else:
                scores_data.append(score.__dict__)
        
        return ApiResponse(
            success=True,
            data=scores_data,
            source=squirrel.source,
            cached=False
        )
    except SquirrelException as e:
        logger.error(f"Error fetching scores: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


