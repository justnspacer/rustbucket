import logging
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException, Query, Depends, status, Body
from squirrel.squirrel_manager import SquirrelManager, SquirrelType
from squirrel.squirrels import SquirrelException
from squirrel.models.jobs_models import JobPosting, JobSearchQuery, Resume
from api.schemas import (
    ApiResponse, JobSearchRequest, JobFilterRequest, ResumeMatchRequest, CoverLetterRequest
)
from .dependencies import get_squirrel_manager

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post(
    "/search",
    response_model=ApiResponse,
    summary="Search for jobs",
    description="Search for job postings using JSearch API. Results are cached for 1 hour."
)
async def search_jobs(
    request: JobSearchRequest,
    apply_filters: bool = Query(True, description="Apply quality filters to results"),
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
        squirrel = manager.get_squirrel(SquirrelType.JOBS)
        
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
        jobs = squirrel.search_jobs(query)
        
        # Apply filters if requested
        if apply_filters:
            jobs = squirrel.filter_jobs(jobs)
        
        return ApiResponse(
            success=True,
            data=[job.to_dict() for job in jobs],
            source="jsearch",
            cached=False  # Could track this from cache
        )
        
    except SquirrelException as e:
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
    "/filter",
    response_model=ApiResponse,
    summary="Filter job postings",
    description="Apply quality filters to a list of job postings."
)
async def filter_jobs(
    jobs: List[Dict] = Body(..., description="List of job postings to filter"),
    filter_options: JobFilterRequest = Body(..., description="Filter options"),
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
        squirrel = manager.get_squirrel(SquirrelType.JOBS)
        
        # Convert dicts to JobPosting objects
        job_objects = [JobPosting.from_dict(job) for job in jobs]
        
        # Apply filters
        filtered_jobs = squirrel.filter_jobs(
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
    "/match",
    response_model=ApiResponse,
    summary="Match resume to jobs",
    description="Match a resume to job postings using TF-IDF similarity scoring."
)
async def match_resume_to_jobs(
    request: ResumeMatchRequest,
    jobs: List[Dict] = Body(..., description="List of job postings to match against"),
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
        squirrel = manager.get_squirrel(SquirrelType.JOBS)
        
        # Create Resume object
        resume = Resume(
            text=request.resume_text,
            file_path="",
            file_type="text"
        )
        
        # Convert dicts to JobPosting objects
        job_objects = [JobPosting.from_dict(job) for job in jobs]
        
        # Match resume to jobs
        matches = squirrel.match_resume_to_jobs(
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
    "/cover-letter",
    response_model=ApiResponse,
    summary="Generate cover letter",
    description="Generate a tailored cover letter using OpenAI GPT-3.5."
)
async def generate_cover_letter(
    request: CoverLetterRequest,
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
        squirrel = manager.get_squirrel(SquirrelType.JOBS)
        
        # Create JobPosting object
        job = JobPosting(
            title=request.job_title,
            company=request.company,
            description=request.job_description,
            url=""
        )
        
        # Generate cover letter
        cover_letter = squirrel.generate_cover_letter(job, request.resume_summary)
        
        return ApiResponse(
            success=True,
            data=cover_letter.to_dict()
        )
        
    except SquirrelException as e:
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
    "/pipeline",
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
    manager: SquirrelManager = Depends(get_squirrel_manager)
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
        squirrel = manager.get_squirrel(SquirrelType.JOBS)
        
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
        jobs = squirrel.search_jobs(query)
        results['jobs'] = [job.to_dict() for job in jobs]
        
        # Step 2: Filter jobs
        filtered_jobs = squirrel.filter_jobs(jobs)
        results['filtered_jobs'] = [job.to_dict() for job in filtered_jobs]
        
        # Step 3: Match resume (if provided)
        if resume_text and filtered_jobs:
            resume = Resume(
                text=resume_text,
                file_path="",
                file_type="text"
            )
            matches = squirrel.match_resume_to_jobs(resume, filtered_jobs, threshold=match_threshold)
            results['matches'] = [match.to_dict() for match in matches]
            
            # Step 4: Generate cover letters (if requested)
            if generate_letters and matches and resume_summary:
                top_matches = matches[:5]  # Top 5 matches
                for match in top_matches:
                    try:
                        cover_letter = squirrel.generate_cover_letter(
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
        
    except SquirrelException as e:
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
