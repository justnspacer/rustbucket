from flask import request
from supabase_client import supabase
from datetime import datetime
from helpers import success_response, error_response, paginated_response
import httpx
from auth import get_spotify_by_user_id, require_spotify_auth, get_spotify_for_current_user

# Authentication errors
AUTH_REQUIRED = "AUTH_REQUIRED"
INVALID_TOKEN = "INVALID_TOKEN"
TOKEN_EXPIRED = "TOKEN_EXPIRED"

# Spotify API errors
SPOTIFY_API_ERROR = "SPOTIFY_API_ERROR"
SPOTIFY_USER_NOT_FOUND = "SPOTIFY_USER_NOT_FOUND"
SPOTIFY_UNAUTHORIZED = "SPOTIFY_UNAUTHORIZED"

# General errors
VALIDATION_ERROR = "VALIDATION_ERROR"
NOT_FOUND = "NOT_FOUND"
INTERNAL_ERROR = "INTERNAL_ERROR"

def get_user_spotify_id(user_id):
    try:
        result = supabase.table('app_spotify').select('spotify_id').eq('user_id', user_id).execute()
        if result.data:
            return result.data[0]['spotify_id']
        return None
    except Exception as e:
        print(f"Error getting Spotify ID for user: {e}")
        return None

def save_or_update_user(spotify_id, user_id):
    try:
        # First check if user exists
        existing_user = supabase.table('app_spotify').select('*').eq('spotify_id', spotify_id).execute()
        
        user_record = {
            'spotify_id': spotify_id,
            'user_id': user_id,
            'linked_at': datetime.now(datetime.timezone.utc).isoformat(),
            'updated_at': datetime.now(datetime.timezone.utc).isoformat()
        }
        
        # Only set created_at for new records
        if not existing_user.data:
            user_record['created_at'] = datetime.now(datetime.timezone.utc).isoformat()
        
        if existing_user.data:
            # Update existing user
            result = supabase.table('app_spotify').update(user_record).eq('spotify_id', spotify_id).execute()
        else:
            # Insert new user
            result = supabase.table('app_spotify').insert(user_record).execute()
        
        return result
    except Exception as e:
        print(f"Error saving user: {e}")
        return None

def search_users(query=None, limit=20):
    try:
        if query:
            # Search by spotify ID only
            result = supabase.table('app_spotify').select('*').ilike('spotify_id', f'%{query}%').limit(limit).execute()
        else:
            # Get all users
            result = supabase.table('app_spotify').select('*').not_.is_('spotify_id', 'null').not_.is_('linked_at', 'null').limit(limit).execute()
        
        return result.data
    except Exception as e:
        print(f"Error searching users: {e}")
        return []

def get_public_user_data(user):
    """Return only public fields for user data"""
    return {
        'spotify_id': user['spotify_id'],
        'images': user.get('images', []),
        'last_updated': user.get('last_updated'),
        'linked_at': user.get('linked_at')
    }

def get_user_info_by_id(user_id):
    try:            
        # Try to get fresh data from Spotify if tokens are available
        sp, access_token, refresh_token = get_spotify_by_user_id(user_id)
        if sp:
            try:
                # Get fresh user info from Spotify
                fresh_user_info = sp.current_user()
                
                # Update Supabase with fresh data
                save_or_update_user(
                    fresh_user_info.get('spotify_id', user_id),
                    fresh_user_info.get('user_id', user_id),
                    linked_at=datetime.datetime.utcnow().isoformat()
                )
                
                return fresh_user_info
            except Exception as e:
                print(f"Failed to get fresh user info for {user_id}: {e}")
                return f"No user for: {user_id}"
        else:
            return "No user found"
            
    except Exception as e:
        print(f"Error getting user info for {user_id}: {e}")
        return None
        
def spotify_endpoints(app):

    @app.route('/api/spotify/profile/<spotify_user_id>')
    @require_spotify_auth
    async def get_spotify_profile(spotify_user_id):
        headers = {'Authorization': f'Bearer {request.spotify_token}'}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f'https://api.spotify.com/v1/users/{spotify_user_id}',
                headers=headers
            )
        return response.json()

    @app.route("/api/spotify")
    def home():
        return success_response(
            data={
            "public_endpoints": [
                "/api/spotify/search-users - Search for users (public access)",
                "/api/spotify/users - List all users (public access)"
            ],
            "authenticated_endpoints": [
                "/api/spotify/u/<user_id> - Get specific user data (requires authentication)",
                "/api/spotify/u/<spotify_id>/top-tracks - User top tracks (requires authentication)",
                "/api/spotify/u/<spotify_id>/top-artists - User top artists (requires authentication)",
                "/api/spotify/u/<spotify_id>/playlists - User playlists (requires authentication)",
                "/api/spotify/u/<spotify_id>/currently-playing - Currently playing (requires authentication)"
            ]
        },
            message="Welcome to the Spotify API integration!"
        )

    @app.route("/api/spotify/search-users")
    def search_spotify_users():
        try:
            query = request.args.get('q', '')
            limit = int(request.args.get('limit', 20))
            users = search_users(query, limit)
            # Return only public data
            public_users = [get_public_user_data(user) for user in users]
            return success_response(
                data={
            'users': public_users,
            'total': len(public_users),
            'query': query,
            },
                message="To view detailed user data, authentication is required."
            )
        except Exception as e:
            return error_response(
                message="Failed to search users",
                status_code=500,
                error_code=SPOTIFY_API_ERROR,
                details={"error": str(e)}
            )

    @app.route("/api/spotify/u/<user_id>")
    @require_spotify_auth
    def get_spotify_id(authenticated_user, user_id):
        
        try:
            user_data = get_user_spotify_id(user_id)

            if not user_data:
                return error_response(
                    message="User not found",
                    status_code=404,
                    error_code=SPOTIFY_USER_NOT_FOUND,
                    details={"user_id": user_id}
                )
            
            # Get user info from Spotify
            user_info = get_user_info_by_id(user_data)
            if not user_info:
                return error_response(
                    message="Failed to get user info from Spotify",
                    status_code=500,
                    error_code=SPOTIFY_API_ERROR,
                    details={"user_id": user_data}
                )
            
            return success_response(
                data={
                    "user_id": user_data,
                    "spotify_info": user_info
                },
                message="User info retrieved successfully"
            )
        except Exception as e:
            return error_response(
                message="Failed to get user info",
                status_code=500,
                error_code=SPOTIFY_API_ERROR,
                details={"error": str(e)}
            )

    @app.route("/api/spotify/top-artists")
    @require_spotify_auth
    def top_artists(authenticated_user):
        try:
            sp, token_info, refresh_info = get_spotify_for_current_user()
            top_artists = sp.current_user_top_artists(limit=20)
            return success_response(
                data={
                    "top_artists": top_artists['items'],
                    "user": authenticated_user['id']
                },
                message="Top artists retrieved successfully"
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve top artists",
                status_code=500,
                error_code=SPOTIFY_API_ERROR,
                details={"error": str(e)}
            )
    
    @app.route("/api/spotify/user-saved-tracks")
    @require_spotify_auth
    def user_saved_tracks(authenticated_user):
        sp, token_info, refresh_info = get_spotify_for_current_user() # Get the Spotify client
        saved_tracks = sp.current_user_saved_tracks(limit=20) # Get the first page of saved tracks
        tracks = [{"name": item["track"]["name"], 
                "artist": item["track"]["artists"][0]["name"], 
                "added_at": datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m.%d.%y"),
                "url": item["track"]["external_urls"]["spotify"]} 
                for item in saved_tracks["items"]]   
        return success_response(
            data={
                "tracks": tracks,
                "user": authenticated_user['id']
            },
            message="User saved tracks retrieved successfully"
        )

    @app.route("/api/spotify/currently-playing")
    @require_spotify_auth
    def currently_playing(authenticated_user):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        current_playback = sp.current_playback(market="US", additional_types=['episode'])
        if current_playback and current_playback['is_playing']:
            return success_response(
                data={
                    "currently_playing": current_playback,
                    "user": authenticated_user['id']
                },
                message="Currently playing track retrieved successfully"
            )
        elif current_playback is None:
            # If no track is currently playing, return a message
            return success_response(
                data={
                    "message": "nothing playing 🎵",
                    "user": authenticated_user['id']
                },
                message="No track currently playing"
            )
        else:
            return error_response(
                message="Failed to retrieve currently playing track",
                status_code=500,
                error_code=SPOTIFY_API_ERROR,
                details={"error": "No track currently playing"}
            )

    @app.route("/api/spotify/top-tracks")
    @require_spotify_auth
    def top_tracks(authenticated_user):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        top_tracks = sp.current_user_top_tracks(limit=20)
        return success_response(
            data={
                "top_tracks": top_tracks['items'],
                "user": authenticated_user['id']
            },
            message="Top tracks retrieved successfully"
        )

    @app.route("/api/spotify/recently-played")
    @require_spotify_auth
    def recently_played(authenticated_user):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        recently_played = sp.current_user_recently_played()
        return success_response(
            data={
                "recently_played": recently_played['items'],
                "user": authenticated_user['id']
            },
            message="Recently played tracks retrieved successfully"
        )

    @app.route("/api/spotify/playlists")
    @require_spotify_auth
    def playlists(authenticated_user):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        playlists = sp.current_user_playlists(limit=20)
        return success_response(
            data={
                "playlists": playlists['items'],
                "user": authenticated_user['id']
            },
            message="Playlists retrieved successfully"
        )

    @app.route("/api/spotify/playlist-tracks/<playlist_id>")
    @require_spotify_auth
    def playlist_tracks(authenticated_user, playlist_id):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        playlist_tracks = sp.playlist_tracks(playlist_id)
        return success_response(
            data={
                "playlist_id": playlist_id,
                "tracks": playlist_tracks['items'],
                "user": authenticated_user['id']
            },
            message="Playlist tracks retrieved successfully"
        )