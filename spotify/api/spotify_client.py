"""
Spotify API client utilities and token management
"""
import base64
import spotipy
from datetime import datetime, timezone
from .database import supabase

def get_spotify_client(access_token):
    """Create Spotify client with access token"""
    return spotipy.Spotify(auth=access_token)

def decode_token(encrypted_token):
    """Decode base64 encoded token"""
    return base64.urlsafe_b64decode(encrypted_token + '==').decode('utf-8')

def encode_token(token):
    """Encode token for storage"""
    return base64.urlsafe_b64encode(token.encode('utf-8')).decode('utf-8').rstrip('=')

def is_token_expired(expires_at_str):
    """Check if token has expired"""
    now = datetime.now(timezone.utc)
    expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
    return now >= expires_at

def handle_spotify_api_error(error):
    """Process Spotify API errors and return appropriate error codes"""
    if error.http_status == 401:
        return "TOKEN_EXPIRED"
    elif error.http_status == 403:
        return "SPOTIFY_UNAUTHORIZED"
    elif error.http_status == 404:
        return "NOT_FOUND"
    elif error.http_status == 429:
        return "RATE_LIMITED"
    else:
        return "SPOTIFY_API_ERROR"
