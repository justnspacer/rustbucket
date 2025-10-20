import os
from supabase import create_client, Client
from typing import List, Optional
from app.schemas.post_schema import PostCreate, PostUpdate
from app.schemas.keyword_schema import KeywordCreate, KeywordUpdate
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    def __init__(self, url: str = None, key: str = None):
        if url is None:
            url = os.getenv("SUPABASE_URL")
        if key is None:
            key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    # ==================== POST METHODS ====================
    
    def fetch_posts(self) -> List[dict]:
        """Fetch all posts with their associated keywords"""
        response = self.supabase.from_('content_blocks').select(
            '*, content_blocks_keywords(keyword_id, keywords(*))'
        ).order('created_at', desc=True).execute()
        
        # Transform the data to include keywords directly
        posts = []
        for post in response.data:
            post_data = {**post}
            # Extract keywords from the join table
            if 'content_blocks_keywords' in post_data:
                post_data['keywords'] = [
                    pk['keywords'] for pk in post_data['content_blocks_keywords'] 
                    if pk.get('keywords')
                ]
                del post_data['content_blocks_keywords']
            else:
                post_data['keywords'] = []
            posts.append(post_data)
        
        return posts

    def get_post(self, post_id: str) -> Optional[dict]:
        """Get a single post with its keywords"""
        response = self.supabase.from_('content_blocks').select(
            '*, content_blocks_keywords(keyword_id, keywords(*))'
        ).eq('id', post_id).execute()
        
        if response.data:
            post_data = {**response.data[0]}
            # Extract keywords from the join table
            if 'content_blocks_keywords' in post_data:
                post_data['keywords'] = [
                    pk['keywords'] for pk in post_data['content_blocks_keywords'] 
                    if pk.get('keywords')
                ]
                del post_data['content_blocks_keywords']
            else:
                post_data['keywords'] = []
            return post_data
        return None

    def create_post(self, post_data: PostCreate) -> dict:
        """Create a new post and optionally link keywords"""
        # Extract keyword_ids before creating post
        keyword_ids = post_data.keyword_ids if hasattr(post_data, 'keyword_ids') else []
        
        # Create the post without keyword_ids
        post_dict = post_data.dict(exclude={'keyword_ids'})
        response = self.supabase.from_('content_blocks').insert(post_dict).execute()
        created_post = response.data[0]
        
        # Link keywords if provided
        if keyword_ids:
            self.link_keywords_to_post(created_post['id'], keyword_ids)
        
        # Return post with keywords
        return self.get_post(created_post['id'])

    def update_post(self, post_id: str, post_data: PostUpdate) -> dict:
        """Update a post and optionally update its keywords"""
        # Extract keyword_ids if provided
        update_dict = post_data.dict(exclude_unset=True)
        keyword_ids = update_dict.pop('keyword_ids', None)
        
        # Update the post
        if update_dict:
            response = self.supabase.from_('content_blocks').update(update_dict).eq('id', post_id).execute()
        
        # Update keywords if provided
        if keyword_ids is not None:
            # Remove existing keyword links
            self.supabase.from_('content_blocks_keywords').delete().eq('content_block_id', post_id).execute()
            # Add new keyword links
            if keyword_ids:
                self.link_keywords_to_post(post_id, keyword_ids)
        
        # Return updated post with keywords
        return self.get_post(post_id)

    def delete_post(self, post_id: str) -> None:
        """Delete a post (cascade will handle content_blocks_keywords if set up in DB)"""
        self.supabase.from_('content_blocks').delete().eq('id', post_id).execute()

    def search_posts(self, query: str) -> List[dict]:
        """Search posts by title with their keywords"""
        response = self.supabase.from_('content_blocks').select(
            '*, content_blocks_keywords(keyword_id, keywords(*))'
        ).ilike('title', f'%{query}%').execute()
        
        # Transform the data to include keywords directly
        posts = []
        for post in response.data:
            post_data = {**post}
            if 'content_blocks_keywords' in post_data:
                post_data['keywords'] = [
                    pk['keywords'] for pk in post_data['content_blocks_keywords'] 
                    if pk.get('keywords')
                ]
                del post_data['content_blocks_keywords']
            else:
                post_data['keywords'] = []
            posts.append(post_data)
        
        return posts

    # ==================== KEYWORD METHODS ====================
    
    def fetch_keywords(self) -> List[dict]:
        """Fetch all keywords"""
        response = self.supabase.from_('keywords').select('*').order('name').execute()
        return response.data
    
    def get_keyword(self, keyword_id: str) -> Optional[dict]:
        """Get a single keyword by ID"""
        response = self.supabase.from_('keywords').select('*').eq('id', keyword_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    def get_keyword_by_name(self, name: str) -> Optional[dict]:
        """Get a keyword by its name (case-insensitive)"""
        response = self.supabase.from_('keywords').select('*').ilike('name', name).execute()
        if response.data:
            return response.data[0]
        return None
    
    def create_keyword(self, keyword_data: KeywordCreate) -> dict:
        """Create a new keyword (check for duplicates first)"""
        # Check if keyword already exists
        existing = self.get_keyword_by_name(keyword_data.name)
        if existing:
            return existing
        
        response = self.supabase.from_('keywords').insert(keyword_data.dict()).execute()
        return response.data[0]
    
    def update_keyword(self, keyword_id: str, keyword_data: KeywordUpdate) -> dict:
        """Update a keyword"""
        response = self.supabase.from_('keywords').update(
            keyword_data.dict(exclude_unset=True)
        ).eq('id', keyword_id).execute()
        return response.data[0]
    
    def delete_keyword(self, keyword_id: str) -> None:
        """Delete a keyword (cascade will handle content_blocks_keywords if set up in DB)"""
        self.supabase.from_('keywords').delete().eq('id', keyword_id).execute()
    
    def link_keywords_to_post(self, post_id: str, keyword_ids: List[str]) -> None:
        """Link multiple keywords to a post"""
        if not keyword_ids:
            return
        
        # Create link records
        links = [{'content_block_id': post_id, 'keyword_id': kid} for kid in keyword_ids]
        self.supabase.from_('content_blocks_keywords').insert(links).execute()
    
    def unlink_keyword_from_post(self, post_id: str, keyword_id: str) -> None:
        """Remove a keyword link from a post"""
        self.supabase.from_('content_blocks_keywords').delete().eq('content_block_id', post_id).eq('keyword_id', keyword_id).execute()
    
    def get_content_blocks_keywords(self, post_id: str) -> List[dict]:
        """Get all keywords for a specific post"""
        response = self.supabase.from_('content_blocks_keywords').select(
            'keywords(*)'
        ).eq('content_block_id', post_id).execute()
        
        return [pk['keywords'] for pk in response.data if pk.get('keywords')]