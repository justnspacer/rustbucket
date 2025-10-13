import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from squirrel.squirrel_manager import SquirrelManager, SquirrelType
from api.schemas import (
    ApiResponse, SourceSwitchRequest, CacheInvalidationRequest,
    SourceInfo
)
from .dependencies import get_squirrel_manager

logger = logging.getLogger(__name__)
router = APIRouter()

# Source management endpoints
@router.get(
    "/sources",
    response_model=List[SourceInfo],
    summary="Get available data sources",
    description="Lists all available data sources for each squirrel type."
)
async def get_sources(
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get available data sources."""
    sources = []
    for squirrel_type in SquirrelType:
        sources.append(SourceInfo(
            squirrel_type=squirrel_type.value,
            active_source=manager.get_active_source(squirrel_type),
            available_sources=manager.get_available_sources(squirrel_type)
        ))
    return sources


@router.post(
    "/sources/switch",
    response_model=ApiResponse,
    summary="Switch data source",
    description="Switches the active data source for a squirrel type."
)
async def switch_source(
    request: SourceSwitchRequest,
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Switch data source."""
    try:
        squirrel_type = SquirrelType(request.squirrel_type)
        manager.switch_source(squirrel_type, request.source)
        
        return ApiResponse(
            success=True,
            data={
                "squirrel_type": request.squirrel_type,
                "new_source": request.source,
                "message": f"Switched {request.squirrel_type} source to {request.source}"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Cache management endpoints
@router.post(
    "/cache/invalidate",
    response_model=ApiResponse,
    summary="Invalidate cache",
    description="Invalidates cache for specified squirrel(s) or cache keys."
)
async def invalidate_cache(
    request: CacheInvalidationRequest,
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Invalidate cache."""
    try:
        squirrel_type = SquirrelType(request.squirrel_type) if request.squirrel_type else None
        manager.invalidate_cache(squirrel_type, request.source, request.cache_key)
        
        message = "Cache invalidated"
        if request.cache_key:
            message += f" for key: {request.cache_key}"
        elif request.squirrel_type:
            message += f" for {request.squirrel_type}"
            if request.source:
                message += f":{request.source}"
        else:
            message += " for all squirrels"
        
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
    description="Clears all cached data for all squirrels."
)
async def clear_cache(
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
    summary="Get squirrel statistics",
    description="Returns statistics about active squirrels and their usage."
)
async def get_stats(
    manager: SquirrelManager = Depends(get_squirrel_manager)
):
    """Get squirrel statistics."""
    return manager.get_squirrel_stats()