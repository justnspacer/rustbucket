from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Dict, Optional
import logging
import time

from routes import user
from auth import verify_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API Gateway", version="1.0.0")

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000", 
    "http://localhost:3001",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service registry
SERVICE_REGISTRY: Dict[str, str] = {
    "git-r-done": "http://127.0.0.1:5000/api/git-r-done",
    "hue-dashboard": "http://127.0.0.1:5000/api/hue-dashboard", 
    "next-rusty-tech": "http://localhost:3000",
    "nothing": "http://127.0.0.1:5000/api/nothing",
    "operator": "http://127.0.0.1:5000/api/operator",
    "spotify": "http://spotify:5000/api/spotify",
}

# Include user routes
app.include_router(user.router)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "message": "API Gateway is running",
        "services": list(SERVICE_REGISTRY.keys())
    }

@app.get("/services")
def list_services():
    """List all available services"""
    return {"services": SERVICE_REGISTRY}

class ProxyService:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    def _prepare_headers(self, original_headers: dict, user_info: Optional[object]) -> dict:
        """Prepare headers for downstream service"""
        headers = {k: v for k, v in original_headers.items() 
                  if k.lower() not in ['host', 'authorization']}
        
        # Add user context if available
        if user_info and hasattr(user_info, 'user'):
            headers.update({
                "x-user-id": str(user_info.user.id),
                "x-user-email": user_info.user.email or "",
                "x-gateway": "true"
            })
        
        return headers
    
    async def forward_request(self, request: Request, target_url: str, user_info: Optional[object]) -> Response:
        """Forward request to target service"""
        headers = self._prepare_headers(dict(request.headers), user_info)
        body = await request.body()
        
        try:
            response = await self.client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body
            )
            
            # Forward response with original headers
            response_headers = dict(response.headers)
            response_headers.pop('content-encoding', None)  # Let FastAPI handle encoding
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=response_headers,
                media_type=response.headers.get('content-type')
            )
            
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        except httpx.TimeoutException:
            logger.error(f"Request timeout to {target_url}")
            raise HTTPException(status_code=504, detail="Gateway timeout")

@app.api_route(
    "/api/{service_name}/{path:path}", 
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
)
async def proxy_to_service(
    service_name: str,
    path: str,
    request: Request,
    user_info=Depends(verify_token)
):
    """Proxy requests to registered services"""
    
    # Get service base URL
    base_url = SERVICE_REGISTRY.get(service_name)
    if not base_url:
        available_services = ", ".join(SERVICE_REGISTRY.keys())
        raise HTTPException(
            status_code=404, 
            detail=f"Service '{service_name}' not found. Available: {available_services}"
        )
    
    # Build target URL
    target_url = f"{base_url}/{path}".rstrip('/')

    
    logger.info(f"Proxying {request.method} {request.url} -> {target_url}")
    
    # Forward request using context manager
    async with ProxyService() as proxy:
        return await proxy.forward_request(request, target_url, user_info)

# Optional: Add middleware for request/response logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}s"
    )
    return response