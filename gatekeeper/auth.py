from jose import jwt
import requests
from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED
import logging
import time
import os
from typing import Optional
import supabase
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
SUPABASE_API_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

security = HTTPBearer()

def retrieve_user(credentials=Depends(security)):
    """Retrieve user information from Supabase using the provided token"""
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
