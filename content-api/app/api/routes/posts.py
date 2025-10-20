from fastapi import APIRouter, HTTPException
from app.schemas.post_schema import Post, PostCreate, PostUpdate
from app.services.supabase_service import SupabaseService
from typing import List

router = APIRouter()
supabase_service = SupabaseService()

@router.post("/posts/", response_model=Post)
def create_post(post: PostCreate):
    created_post = supabase_service.create_post(post)
    if not created_post:
        raise HTTPException(status_code=400, detail="Error creating post")
    return created_post

@router.get("/posts/", response_model=List[Post])
def get_posts():
    posts = supabase_service.fetch_posts()
    return posts

@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: str):
    post = supabase_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: str, post: PostUpdate):
    updated_post = supabase_service.update_post(post_id, post)
    if not updated_post:
        raise HTTPException(status_code=400, detail="Error updating post")
    return updated_post

@router.delete("/posts/{post_id}")
def delete_post(post_id: str):
    supabase_service.delete_post(post_id)
    return {"message": "Post deleted successfully"}