from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.post_schema import Post
from app.services.supabase_service import SupabaseService

router = APIRouter()
supabase_service = SupabaseService()

@router.get("/search", response_model=List[Post])
def search(query: str):
    results = supabase_service.search_posts(query)
    if not results:
        raise HTTPException(status_code=404, detail="No posts found")
    return results