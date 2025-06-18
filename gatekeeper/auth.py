import os
from jose import jwt
import requests
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from dotenv import load_dotenv

load_dotenv()

SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
if not SUPABASE_PROJECT_ID:
    raise RuntimeError("SUPABASE_PROJECT_ID environment variable is not set.")

JWKS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/keys"

security = HTTPBearer()
try:
    jwks = requests.get(JWKS_URL).json()
except requests.exceptions.RequestException as e:
    raise RuntimeError(f"Failed to fetch JWKS: {e}")

def verify_token(request: Request, credentials=Depends(security)):
    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == unverified_header["kid"]), None)
        if key is None:
            raise Exception("Key not found")

        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
        payload = jwt.decode(token, public_key, algorithms=["RS256"])

        request.state.user_id = payload["sub"]
        return payload
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"Token verification failed: {e}")
