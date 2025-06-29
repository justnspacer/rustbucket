from fastapi import FastAPI
from routes import user
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
import httpx
from auth import verify_token

app = FastAPI()

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
async def route_to_service(service: str, path: str, request: Request, token=Depends(verify_token)):
    base_url = ROUTING_TABLE.get(service)
    if not base_url:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    target_url = f"{base_url}/{path}"
    return await proxy_request(request, target_url)

async def proxy_request(request: Request, target_url: str):
    method = request.method
    headers = dict(request.headers)
    headers["x-user-id"] = request.state.user_id

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=method,
            url=target_url,
            headers=headers,
            content=await request.body()
        )

    return JSONResponse(status_code=response.status_code, content=response.json())

print("Gatekeeper is running...")

