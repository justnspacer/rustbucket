from fastapi import FastAPI
from routes import user
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
import httpx
from auth import verify_token

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js app
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative Next.js port
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": 
    "Welcome to the API Gateway. Use the /api/{service}/{path} endpoint to access services."}   

ROUTING_TABLE = {
    "git-r-done": "http://127.0.0.1:5000/git-r-done",
    "hue-dashboard": "http://127.0.0.1:5000/hue-dashboard",
    "next-rusty-tech": "http://localhost:3000",
    "nothing": "http://127.0.0.1:5000/nothing",                
    "operator": "http://127.0.0.1:5000/operator",                    
    "spotify": "http://127.0.0.1:5000/spotify",
}

@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_to_service(service: str, path: str, request: Request, user_response=Depends(verify_token)):
    base_url = ROUTING_TABLE.get(service)
    if not base_url:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    target_url = f"{base_url}/{path}"
    return await proxy_request(request, target_url, user_response)

async def proxy_request(request: Request, target_url: str, user_response):
    method = request.method
    headers = dict(request.headers)
    
    # Add user information to headers for downstream services
    if user_response and user_response.user:
        headers["x-user-id"] = user_response.user.id
        headers["x-user-email"] = user_response.user.email or ""
        headers["x-user-metadata"] = str(user_response.user.user_metadata or {})
    
    # Remove authorization header to prevent conflicts
    headers.pop("authorization", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=await request.body(),
            timeout=30.0
        )

    return JSONResponse(status_code=response.status_code, content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text)

print("Gatekeeper is running...")

