import logging
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from scraper_please.scraper_manager import ScraperManager, ScraperType
from api.schemas import (
    ApiResponse, SourceSwitchRequest, CacheInvalidationRequest,
    SourceInfo
)
from .dependencies import get_scraper_manager

logger = logging.getLogger(__name__)
router = APIRouter()

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