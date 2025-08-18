import base64
from hashlib import sha256
from flask import request, redirect, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import requests
from supabase_client import supabase
import json
from datetime import datetime
from spotify.helpers import success_response, error_response, paginated_response
import random
import string
from functools import wraps
import httpx
import token_manager

load_dotenv()

def register_spotify_routes(app, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL, SCOPE):

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
    
    """helper function to register Spotify-related routes"""
    def get_authenticated_user(request):
        """Extract authenticated user info from request headers"""
        user_id = request.headers.get('x-user-id')
        user_email = request.headers.get('x-user-email')
        user_metadata = request.headers.get('x-user-metadata')
        
        if user_id:
            user_data = {
                'id': user_id,
                'email': user_email,
                'metadata': {}
            }
            
            # Parse metadata if present
            if user_metadata:
                try:
                    user_data['metadata'] = json.loads(user_metadata.replace("'", '"'))
                except:
                    pass
            
            return user_data
        return None

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

    def get_user(spotify_id):
        """Get a specific user by spotify_id"""
        try:
            result = supabase.table('app_spotify').select('*').eq('spotify_id', spotify_id).not_.is_('spotify_id', 'null').not_.is_('linked_at', 'null').execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def get_public_user_data(user):
        """Return only public fields for user data"""
        return {
            'spotify_id': user['spotify_id'],
            'followers': user.get('followers', 0),
            'images': user.get('images', []),
            'country': user.get('country'),
            'product': user.get('product'),
            'last_updated': user.get('last_updated'),
            'linked_at': user.get('linked_at')
        }

    oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI, 
                        scope=SCOPE)

    def refresh_spotify_token(refresh_token, client_id, client_secret):
        url = TOKEN_URL
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'Authorization': f'Basic {client_id}:{client_secret}'
        }

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Failed to refresh token')

    def get_spotify_for_current_user():
        token_info = oauth.get_access_token()
        sp = spotipy.Spotify(auth=token_info["access_token"])    
        # Check if the token has expired
        now = datetime.now()
        expires_at = datetime.fromtimestamp(token_info['expires_at'])
        if now >= expires_at:
            # Refresh the token
            refresh_token = token_info['refresh_token']
            new_access_token = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
            token_info['access_token'] = new_access_token
            token_info['expires_at'] = (now + datetime.timedelta(seconds=3600)).timestamp() #1 hour variable, move to env
            cache_handler.save_token_to_cache(token_info)
        return sp, token_info["access_token"], token_info["refresh_token"]    

    def get_spotify_by_user_id(user_id):
        """Get Spotify client and user info for a specific user ID from Supabase"""
        try:
            # Get user data from Supabase
            user_data = get_user(user_id)
            if not user_data:
                return None, None, None
            
            # access_token = user_data.get('access_token')
            access_token = "BQCcyOlwFQZlvD6z46hIbuNK0xN_uaYdKhBNDb8qlelspCcwPJGnCk5yFJ2T3ceeOEAbd3ueFl07kkyxWifdm4IEkNTG0zDGyZG4WUGZX939UnpbNRRH9Xc_tBRre1KvivGTj-Na39AoUayIGZfq9EMyPMSQAm8HE19mPnaF4LYdIVBEAIkGA3gML6hl7-jFsy3FVOpT4ufbQ7BRszvum_YLm-IaWz5bYVA4_knwsmViWFGaYON9QMtW_XjSNSmDBQIbsF5EwrNoziaB60Gi"
            refresh_token = user_data.get('refresh_token')
            
            if not access_token:
                return None, None, None
            
            # Create Spotify client with the user's access token
            sp = spotipy.Spotify(auth=access_token)
            
            # Check if token is still valid by trying to get user info
            try:
                user_info = sp.current_user()
                return sp, access_token, refresh_token
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 401:  # Unauthorized - token expired
                    # Try to refresh the token
                    if refresh_token:
                        try:
                            new_access_token = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
                            
                            # Update token in Supabase
                            supabase.table('app_spotify').update({
                                'access_token': new_access_token,
                                'last_updated': datetime.datetime.utcnow().isoformat()
                            }).eq('spotify_id', user_id).execute()
                            
                            # Create new Spotify client with refreshed token
                            sp = spotipy.Spotify(auth=new_access_token)
                            return sp, new_access_token, refresh_token
                        except Exception as refresh_error:
                            print(f"Failed to refresh token for user {user_id}: {refresh_error}")
                            return None, None, None
                return None, None, None
        except Exception as e:
            print(f"Error getting Spotify client for user {user_id}: {e}")
            return None, None, None

    def get_user_info_by_id(user_id):
        try:
            cached_data = get_user(user_id)
            if not cached_data:
                return None
            
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
                    # Fall back to cached data
                    return cached_data
            else:
                # Return cached data from Supabase
                return cached_data
                
        except Exception as e:
            print(f"Error getting user info for {user_id}: {e}")
            return None
        
    def generate_random_string(length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def base64_url_encode(data):
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')
    
    def store_temp_oauth_data(user_id, data):
        """Store temporary OAuth data in Supabase"""
        try:
            result = supabase.table('app_spotify').insert({
                'user_id': user_id,
                'data': json.dumps(data),
                'created_at': datetime.datetime.utcnow().isoformat()
            }).execute()
            return result
        except Exception as e:
            print(f"Error storing temporary OAuth data: {e}")
            return None
    
    class TokenNotFoundError(Exception):
        """Custom exception for when a token is not found."""
        pass
    
    def require_spotify_auth(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # Get authenticated user from Supabase
            user = await get_authenticated_user(request)
            if not user:
                return {"error": "Authentication required"}, 401
            
            # Get valid Spotify token
            try:
                spotify_token = await token_manager.get_valid_token(user['id'])
            except TokenNotFoundError:
                return {"error": "Spotify authorization required"}, 403
            
            # Add token to request context
            request.spotify_token = spotify_token
            return await f(*args, **kwargs)
        
        return decorated_function

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

    """Register Spotify-related routes"""
    @app.route("/api/spotify/authorize")
    async def spotify_authorize():
        state = generate_random_string(16)
        code_verifier = generate_random_string(128)
        code_challenge = base64_url_encode(sha256(code_verifier))

        await store_temp_oauth_data(user_id, {
            'state': state,
            'code_verifier': code_verifier
        })

        auth_url = f"https://accounts.spotify.com/authorize?" \
               f"client_id={CLIENT_ID}&" \
               f"response_type=code&" \
               f"redirect_uri={REDIRECT_URI}&" \
               f"code_challenge_method=S256&" \
               f"code_challenge={code_challenge}&" \
               f"state={state}&" \
               f"scope=user-read-private user-read-email"
    
        return redirect(auth_url)

    @app.route("/api/spotify/login")
    def login():
        auth_url = oauth.get_authorize_url()
        return redirect(auth_url)

    @app.route("/api/spotify/request-token")
    def request_token():
        code = request.args.get("code")
        token_info = oauth.get_access_token(code)
        return jsonify(token_info)

    @app.route("/api/spotify/callback")
    def callback():
        try:
            if 'token_info' in session:
                return jsonify(session['token_info'])
        except Exception as e:
            print(f"Error retrieving token from session: {e}")
    
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