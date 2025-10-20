from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.keyword_schema import Keyword, KeywordCreate, KeywordUpdate, PostKeywordLink
from app.services.supabase_service import SupabaseService

router = APIRouter()
supabase_service = SupabaseService()

@router.post("/keywords/", response_model=Keyword)
def create_keyword(keyword: KeywordCreate):
    """Create a new keyword or return existing one if name already exists"""
    try:
        created_keyword = supabase_service.create_keyword(keyword)
        return created_keyword
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating keyword: {str(e)}")

@router.get("/keywords/", response_model=List[Keyword])
def get_keywords():
    """Get all keywords"""
    try:
        keywords = supabase_service.fetch_keywords()
        return keywords
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching keywords: {str(e)}")

@router.get("/keywords/{keyword_id}", response_model=Keyword)
def get_keyword(keyword_id: str):
    """Get a specific keyword by ID"""
    keyword = supabase_service.get_keyword(keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@router.get("/keywords/by-name/{name}", response_model=Keyword)
def get_keyword_by_name(name: str):
    """Get a keyword by its name"""
    keyword = supabase_service.get_keyword_by_name(name)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword

@router.put("/keywords/{keyword_id}", response_model=Keyword)
def update_keyword(keyword_id: str, keyword: KeywordUpdate):
    """Update a keyword"""
    try:
        updated_keyword = supabase_service.update_keyword(keyword_id, keyword)
        if not updated_keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return updated_keyword
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating keyword: {str(e)}")

@router.delete("/keywords/{keyword_id}")
def delete_keyword(keyword_id: str):
    """Delete a keyword"""
    try:
        supabase_service.delete_keyword(keyword_id)
        return {"message": "Keyword deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting keyword: {str(e)}")

@router.post("/posts/{post_id}/keywords")
def link_keywords_to_post(post_id: str, keyword_ids: List[str]):
    """Link existing keywords to a post"""
    try:
        supabase_service.link_keywords_to_post(post_id, keyword_ids)
        return {"message": f"Successfully linked {len(keyword_ids)} keywords to post"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error linking keywords: {str(e)}")

@router.delete("/posts/{post_id}/keywords/{keyword_id}")
def unlink_keyword_from_post(post_id: str, keyword_id: str):
    """Remove a keyword link from a post"""
    try:
        supabase_service.unlink_keyword_from_post(post_id, keyword_id)
        return {"message": "Keyword unlinked from post successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error unlinking keyword: {str(e)}")

@router.get("/posts/{post_id}/keywords", response_model=List[Keyword])
def get_content_blocks_keywords(post_id: str):
    """Get all keywords for a specific post"""
    try:
        keywords = supabase_service.get_content_blocks_keywords(post_id)
        return keywords
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching post keywords: {str(e)}")
