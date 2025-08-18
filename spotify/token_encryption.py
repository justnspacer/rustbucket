import os
from datetime import datetime
from datetime import timedelta
from supabase_client import supabase
from token_manager import SpotifyTokenManager
from cryptography.fernet import Fernet

class TokenEncryption:
    def __init__(self):
        # Store this key securely (environment variable)
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher = Fernet(self.key)
    
    def encrypt_token(self, token: str) -> str:
        return self.cipher.encrypt(token.encode()).decode()
    
    def decrypt_token(self, encrypted_token: str) -> str:
        return self.cipher.decrypt(encrypted_token.encode()).decode()

# Usage
encryptor = TokenEncryption()

async def store_spotify_tokens(user_id: str, access_token: str, 
                             refresh_token: str, expires_in: int):
    encrypted_access = encryptor.encrypt_token(access_token)
    encrypted_refresh = encryptor.encrypt_token(refresh_token)
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
    
    # Store in Supabase
    await supabase.table('app_spotify').upsert({
        'user_id': user_id,
        'encrypted_access_token': encrypted_access,
        'encrypted_refresh_token': encrypted_refresh,
        'expires_at': expires_at.isoformat()
    }).execute()