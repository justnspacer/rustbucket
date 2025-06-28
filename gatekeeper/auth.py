import os
from jose import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
import logging
import supabase
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

security = HTTPBearer()

async def verify_token(credentials=Depends(security)):
    try:
        token = credentials.credentials
        response = supabase.auth.get_user(token)
        return response
    except Exception as e:
        logging.error(f"Failed to retrieve user: {e}")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, 
            detail=f"Failed to retrieve user: {e}"
        )