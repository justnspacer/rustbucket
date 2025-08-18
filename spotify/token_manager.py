from datetime import datetime
from datetime import timedelta

class TokenNotFoundError(Exception):
    """Custom exception for when a token is not found."""
    pass

class SpotifyTokenManager:
    def __init__(self, supabase_client, encryptor):
        self.supabase = supabase_client
        self.encryptor = encryptor
    
    async def get_valid_token(self, user_id: str) -> str:
        # Get token from database
        result = await self.supabase.table('app_spotify')\
            .select('*')\
            .eq('user_id', user_id)\
            .single()\
            .execute()
        
        if not result.data:
            raise TokenNotFoundError("No Spotify token found for user")
        
        token_data = result.data
        expires_at = datetime.fromisoformat(token_data['expires_at'])
        
        # Check if token is expired
        if datetime.now(datetime.timezone.utc) >= expires_at:
            return await self.refresh_token(user_id, token_data)
        
        return self.encryptor.decrypt_token(
            token_data['encrypted_access_token']
        )
    
    async def refresh_token(self, user_id: str, token_data: dict) -> str:
        refresh_token = self.encryptor.decrypt_token(
            token_data['encrypted_refresh_token']
        )
        
        # Call Spotify refresh endpoint
        response = await self.spotify_refresh_request(refresh_token)
        
        # Update stored tokens
        await self.store_refreshed_tokens(user_id, response)
        
        return response['access_token']