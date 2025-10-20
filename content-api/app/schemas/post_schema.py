from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    body: str  # Actual DB column name
    user_id: str  # Actual DB column name
    layout: Optional[str] = None
    media_type: Optional[str] = None
    media_urls: Optional[List[str]] = []
    is_published: Optional[bool] = True
    keyword_ids: Optional[List[str]] = []

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    user_id: Optional[str] = None
    layout: Optional[str] = None
    media_type: Optional[str] = None
    media_urls: Optional[List[str]] = None
    is_published: Optional[bool] = None
    keyword_ids: Optional[List[str]] = None

class Post(BaseModel):
    id: str
    title: str
    body: str
    user_id: str
    layout: Optional[str] = None
    media_type: Optional[str] = None
    media_urls: Optional[List[str]] = []
    is_published: Optional[bool] = True
    created_at: datetime
    updated_at: datetime
    keywords: List[dict] = Field(default_factory=list)

    class Config:
        from_attributes = True