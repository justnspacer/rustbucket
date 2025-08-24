from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY

# Supabase client (initialized on first use)
_supabase_client = None

def get_supabase_client():
    """Get or initialize Supabase client"""
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise Exception("Supabase credentials not configured")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

# For backwards compatibility
supabase = get_supabase_client

def get_user_by_spotify_id(spotify_id):
    """Get user data by Spotify ID"""
    try:
        client = get_supabase_client()
        result = client.table('app_spotify').select('*').eq('spotify_id', spotify_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting user by spotify_id: {e}")
        return None

def get_user_by_supabase_id(user_id):
    """Get user's Spotify data by Supabase user ID"""
    try:
        client = get_supabase_client()
        result = client.table('app_spotify').select('*').eq('user_id', user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting user by user_id: {e}")
        return None

def cleanup_expired_oauth_states():
    """Clean up expired OAuth states (called by cron job)"""
    from datetime import datetime, timezone
    try:
        client = get_supabase_client()
        current_time = datetime.now(timezone.utc).isoformat()
        result = client.table('temp_oauth_state').delete().lt('expires_at', current_time).execute()
        return len(result.data) if result.data else 0
    except Exception as e:
        print(f"Error cleaning up OAuth states: {e}")
        return 0
