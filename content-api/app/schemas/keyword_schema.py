from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class KeywordCreate(BaseModel):
    name: str
    
class KeywordUpdate(BaseModel):
    name: Optional[str] = None

class Keyword(BaseModel):
    id: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostKeywordLink(BaseModel):
    """Schema for linking keywords to posts"""
    keyword_ids: list[str]
