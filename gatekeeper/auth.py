import os
from jose import jwt
import requests
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv
import time

load_dotenv()

SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
JWKS_URL = f"https://{SUPABASE_PROJECT_ID}{os.getenv("JWKS_URL_DOMAIN")}"
CACHE_TTL_SECONDS = os.getenv("CACHE_TTL_SECONDS")

security = HTTPBearer()

_cached_jwks = None
_cached_time = 0

def verify_token(request: Request, credentials=Depends(security)):
    token = credentials.credentials
    jwks = get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
        print("JWKS Response:", jwks)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
        if key is None:
            raise Exception("Key not found")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        request.state.user_id = payload["sub"]
        print(f"Authenticated user: {request.state.user_id}")
        return payload
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"Token verification failed: {e}")

def get_jwks():
    global _cached_jwks, _cached_time
    if _cached_jwks is None or (time.time() - _cached_time) > CACHE_TTL_SECONDS:
        headers = {"apikey": SUPABASE_ANON_KEY}
        response = requests.get(JWKS_URL, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch JWKS")
        data = response.json()
        if "keys" not in data:
            raise HTTPException(status_code=500, detail="Invalid JWKS format")
        _cached_jwks = data
        _cached_time = time.time()
    return _cached_jwks