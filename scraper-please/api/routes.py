"""
API routes for the scraper service.
"""
import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends, status, Body, UploadFile, File

from scraper_please.scraper_manager import ScraperManager, ScraperType
from scraper_please.scrapers import ScraperException, DataNotFoundException
from scraper_please.models.foolsball_models import Team, Player, GameScore, PlayerStats
from scraper_please.models.jobs_models import JobPosting, JobSearchQuery, Resume
from api.schemas import (
    ApiResponse, TeamResponse, PlayerResponse, GameScoreResponse,
    PlayerStatsResponse, SourceSwitchRequest, CacheInvalidationRequest,
    SourceInfo, PlayerStatsRequest, ErrorResponse,
    JobSearchRequest, JobFilterRequest, ResumeMatchRequest, CoverLetterRequest,
    JobResponse, JobMatchResponse, CoverLetterResponse
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


# ============================================================================
# JOB SCRAPER ENDPOINTS
# ============================================================================

@router.post(
    "/jobs/search",
    response_model=ApiResponse,
    summary="Search for jobs",
    description="Search for job postings using JSearch API. Results are cached for 1 hour."
)
async def search_jobs(
    request: JobSearchRequest,
    apply_filters: bool = Query(True, description="Apply quality filters to results"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """
    Search for jobs with optional filtering.
    
    - **keywords**: Search terms (e.g., "Python developer")
    - **location**: Job location (optional)
    - **page**: Page number (default: 1)
    - **num_pages**: Number of pages to fetch (default: 1, max: 10)
    - **apply_filters**: Whether to apply quality filters (default: True)
    """
    try:
        scraper = manager.get_scraper(ScraperType.JOBS)
        
        # Create query object
        query = JobSearchQuery(
            keywords=request.keywords,
            location=request.location,
            page=request.page,
            num_pages=request.num_pages,
            country=request.country,
            date_posted=request.date_posted,
            employment_type=request.employment_type,
            remote_jobs_only=request.remote_jobs_only
        )
        
        # Search for jobs
        jobs = scraper.search_jobs(query)
        
        # Apply filters if requested
        if apply_filters:
            jobs = scraper.filter_jobs(jobs)
        
        return ApiResponse(
            success=True,
            data=[job.to_dict() for job in jobs],
            source="jsearch",
            cached=False  # Could track this from cache
        )
        
    except ScraperException as e:
        logger.error(f"Error searching jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in job search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/jobs/filter",
    response_model=ApiResponse,
    summary="Filter job postings",
    description="Apply quality filters to a list of job postings."
)
async def filter_jobs(
    jobs: List[Dict] = Body(..., description="List of job postings to filter"),
    filter_options: JobFilterRequest = Body(..., description="Filter options"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """
    Filter job postings based on quality criteria.
    
    Filters include:
    - **remove_duplicates**: Remove duplicate postings (based on content hash)
    - **check_red_flags**: Filter out jobs with suspicious terms
    - **trusted_only**: Only include jobs from trusted domains
    - **validate_description**: Filter out low-quality descriptions
    """
    try:
        scraper = manager.get_scraper(ScraperType.JOBS)
        
        # Convert dicts to JobPosting objects
        job_objects = [JobPosting.from_dict(job) for job in jobs]
        
        # Apply filters
        filtered_jobs = scraper.filter_jobs(
            job_objects,
            remove_duplicates=filter_options.remove_duplicates,
            check_red_flags=filter_options.check_red_flags,
            trusted_only=filter_options.trusted_only,
            validate_description=filter_options.validate_description
        )
        
        return ApiResponse(
            success=True,
            data={
                "original_count": len(job_objects),
                "filtered_count": len(filtered_jobs),
                "removed_count": len(job_objects) - len(filtered_jobs),
                "jobs": [job.to_dict() for job in filtered_jobs]
            }
        )
        
    except Exception as e:
        logger.error(f"Error filtering jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/jobs/match",
    response_model=ApiResponse,
    summary="Match resume to jobs",
    description="Match a resume to job postings using TF-IDF similarity scoring."
)
async def match_resume_to_jobs(
    request: ResumeMatchRequest,
    jobs: List[Dict] = Body(..., description="List of job postings to match against"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """
    Match resume to job postings.
    
    Uses TF-IDF vectorization and cosine similarity to score matches.
    
    - **resume_text**: Full resume text content
    - **threshold**: Minimum match score (0.0 to 1.0, default: 0.2)
    - **jobs**: List of job postings to match against
    
    Returns jobs sorted by match score (highest first).
    """
    try:
        scraper = manager.get_scraper(ScraperType.JOBS)
        
        # Create Resume object
        resume = Resume(
            text=request.resume_text,
            file_path="",
            file_type="text"
        )
        
        # Convert dicts to JobPosting objects
        job_objects = [JobPosting.from_dict(job) for job in jobs]
        
        # Match resume to jobs
        matches = scraper.match_resume_to_jobs(
            resume,
            job_objects,
            threshold=request.threshold
        )
        
        return ApiResponse(
            success=True,
            data={
                "total_jobs": len(job_objects),
                "matches_found": len(matches),
                "threshold": request.threshold,
                "matches": [match.to_dict() for match in matches]
            }
        )
        
    except Exception as e:
        logger.error(f"Error matching resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/jobs/cover-letter",
    response_model=ApiResponse,
    summary="Generate cover letter",
    description="Generate a tailored cover letter using OpenAI GPT-3.5."
)
async def generate_cover_letter(
    request: CoverLetterRequest,
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """
    Generate a cover letter for a job posting.
    
    Uses OpenAI's GPT-3.5 to generate a professional, tailored cover letter.
    
    - **job_title**: Position title
    - **company**: Company name
    - **job_description**: Full job description
    - **resume_summary**: Brief summary of candidate's experience
    
    Requires OPENAI_API_KEY to be configured.
    """
    try:
        scraper = manager.get_scraper(ScraperType.JOBS)
        
        # Create JobPosting object
        job = JobPosting(
            title=request.job_title,
            company=request.company,
            description=request.job_description,
            url=""
        )
        
        # Generate cover letter
        cover_letter = scraper.generate_cover_letter(job, request.resume_summary)
        
        return ApiResponse(
            success=True,
            data=cover_letter.to_dict()
        )
        
    except ScraperException as e:
        if "API key not configured" in str(e):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OpenAI API key not configured. Cover letter generation is unavailable."
            )
        logger.error(f"Error generating cover letter: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error generating cover letter: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/jobs/pipeline",
    response_model=ApiResponse,
    summary="Run full job search pipeline",
    description="Complete workflow: search, filter, match resume, and generate cover letters."
)
async def run_job_pipeline(
    search_request: JobSearchRequest,
    resume_text: Optional[str] = Body(None, description="Resume text for matching (optional)"),
    resume_summary: Optional[str] = Body(None, description="Resume summary for cover letters (optional)"),
    generate_letters: bool = Body(False, description="Generate cover letters for top matches"),
    match_threshold: float = Body(0.2, ge=0.0, le=1.0, description="Minimum match score threshold"),
    manager: ScraperManager = Depends(get_scraper_manager)
):
    """
    Run complete job search pipeline.
    
    Steps:
    1. Search for jobs using provided criteria
    2. Filter jobs for quality
    3. Match resume to jobs (if resume_text provided)
    4. Generate cover letters for top 5 matches (if requested)
    
    Returns comprehensive results including all steps.
    """
    try:
        scraper = manager.get_scraper(ScraperType.JOBS)
        
        # Create query object
        query = JobSearchQuery(
            keywords=search_request.keywords,
            location=search_request.location,
            page=search_request.page,
            num_pages=search_request.num_pages,
            country=search_request.country,
            date_posted=search_request.date_posted,
            employment_type=search_request.employment_type,
            remote_jobs_only=search_request.remote_jobs_only
        )
        
        results = {
            'jobs': [],
            'filtered_jobs': [],
            'matches': [],
            'cover_letters': []
        }
        
        # Step 1: Search for jobs
        jobs = scraper.search_jobs(query)
        results['jobs'] = [job.to_dict() for job in jobs]
        
        # Step 2: Filter jobs
        filtered_jobs = scraper.filter_jobs(jobs)
        results['filtered_jobs'] = [job.to_dict() for job in filtered_jobs]
        
        # Step 3: Match resume (if provided)
        if resume_text and filtered_jobs:
            resume = Resume(
                text=resume_text,
                file_path="",
                file_type="text"
            )
            matches = scraper.match_resume_to_jobs(resume, filtered_jobs, threshold=match_threshold)
            results['matches'] = [match.to_dict() for match in matches]
            
            # Step 4: Generate cover letters (if requested)
            if generate_letters and matches and resume_summary:
                top_matches = matches[:5]  # Top 5 matches
                for match in top_matches:
                    try:
                        cover_letter = scraper.generate_cover_letter(
                            match.job,
                            resume_summary
                        )
                        results['cover_letters'].append(cover_letter.to_dict())
                    except Exception as e:
                        logger.warning(f"Cover letter generation failed for {match.job.title}: {e}")
                        continue
        
        return ApiResponse(
            success=True,
            data={
                "summary": {
                    "total_jobs_found": len(results['jobs']),
                    "jobs_after_filtering": len(results['filtered_jobs']),
                    "resume_matches": len(results['matches']),
                    "cover_letters_generated": len(results['cover_letters'])
                },
                "results": results
            }
        )
        
    except ScraperException as e:
        logger.error(f"Error in job pipeline: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in job pipeline: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
