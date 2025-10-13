"""
FastAPI application for the squirrel service.
Provides REST API endpoints for search NFL data with caching and source switching.
"""
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from squirrel.squirrel_manager import SquirrelManager
from squirrel import __version__
from api.routes import router
from api.schemas import HealthResponse, ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global squirrel manager instance
squirrel_manager: SquirrelManager = None


# Create FastAPI application
app = FastAPI(
    title="Squirrel API",
    description="A flexible web search API",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup."""
    global squirrel_manager
    
    logger.info("Starting squirrel service...")
    squirrel_manager = SquirrelManager(
        cache_enabled=True,
        rate_limit_enabled=True
    )
    logger.info("Squirrel manager initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    global squirrel_manager
    
    logger.info("Shutting down squirrel service...")
    if squirrel_manager:
        squirrel_manager.close_all()
    logger.info("Squirrel service shutdown complete")


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


# Root endpoints
@app.get("/", summary="Root endpoint")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Squirrel API",
        "version": __version__,
        "description": "A flexible web search API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """Health check endpoint."""
    stats = squirrel_manager.get_squirrel_stats() if squirrel_manager else None
    
    return HealthResponse(
        status="healthy",
        version=__version__,
        squirrel_stats=stats
    )


# Include API routes
app.include_router(
    router,
    prefix="/api/v1"
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - {response.status_code}")
    return response


def main():
    """Run the FastAPI application."""
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )


if __name__ == "__main__":
    main()
