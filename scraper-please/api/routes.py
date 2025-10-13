from fastapi import APIRouter
from .routes_nfl import router as nfl_router
from .routes_jobs import router as job_router
from .routes_system import router as system_router

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(nfl_router, prefix="/foolsball", tags=["Foolsball"])
router.include_router(job_router, prefix="/jobs", tags=["Jobs"])
router.include_router(system_router, tags=["System"])