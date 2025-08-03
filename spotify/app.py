import datetime
from flask import Flask, request, redirect, session, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import requests, os
from supabase_client import supabase
import json
from datetime import datetime
from flask_cors import CORS

load_dotenv()

def register_spotify_routes(app, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL, SCOPE, DEVICE_ID):
    """helper function to register Spotify-related routes"""

    def get_authenticated_user_from_headers():
        """Extract authenticated user info from gatekeeper headers"""
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
            result = supabase.table('app_spotify').select('spotify_id').eq('supabase_user_id', user_id).execute()
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
                'supabase_user_id': user_id,
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

    def require_authenticated_user(f):
        """Decorator to require authenticated user from gatekeeper"""
        def decorated_function(*args, **kwargs):
            user = get_authenticated_user_from_headers()
            if not user:
                return jsonify({"error": "Authentication required"}), 401
            return f(user, *args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function


    cache_handler = CacheFileHandler(cache_path=".cache")
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
        now = datetime.datetime.now()
        expires_at = datetime.datetime.fromtimestamp(token_info['expires_at'])
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
            
            access_token = user_data.get('access_token')
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
                        fresh_user_info.get('supabase_user_id', user_id),
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
        
    """Register Spotify-related routes"""
    @app.route("/api/spotify")
    def home():
        return jsonify({"message": "Welcome to the Spotify API integration! Use the endpoints to interact with your Spotify data."})
    
    # Get spotify id by user id
    @app.route("/api/spotify/u/<user_id>")
    def get_spotify_id(user_id):

        user_data = get_user_spotify_id(user_id)
        print(f"User data for {user_id}: {user_data}")
        if not user_data:
            return jsonify({"error": "User not found or hasn't authorized this app"}), 404
        
        # Get user info from Spotify
        user_info = get_user_info_by_id(user_data)
        if not user_info:
            return jsonify({"error": "Spotify user data not found"}), 404
        
        
        return jsonify({"spotify_id": user_data})

    @app.route("/api/spotify/search-users")
    def search_spotify_users():
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 20))
        
        users = search_users(query, limit)
        
        # Return only public data
        public_users = []
        for user in users:
            public_users.append({
                'spotify_id': user['spotify_id'],
                'followers': user.get('followers', 0),
                'images': user.get('images', []),
                'country': user.get('country'),
                'product': user.get('product'),
                'last_updated': user.get('last_updated')
            })
        
        return jsonify({
            'users': public_users,
            'total': len(public_users),
            'query': query
        })

    @app.route("/api/spotify/users")
    def list_users():
        limit = int(request.args.get('limit', 20))
        users = search_users(limit=limit)
        
        # Return only public data
        public_users = []
        for user in users:
            public_users.append({
                'spotify_id': user['spotify_id'],
                'followers': user.get('followers', 0),
                'images': user.get('images', []),
                'country': user.get('country'),
                'product': user.get('product'),
                'last_updated': user.get('last_updated')
            })
        
        return jsonify({
            'users': public_users,
            'total': len(public_users)
        })

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
        code = request.args.get("code")
        token_info = oauth.get_access_token(code)
        session["token_info"] = token_info
        return jsonify(token_info)

    @app.route("/api/spotify/top-artists-and-tracks")
    def top_artists_and_tracks():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        top_artists = sp.current_user_top_artists(limit=20)
        top_tracks = sp.current_user_top_tracks(limit=20)
        return jsonify({
            "top_artists": top_artists['items'],
            "top_tracks": top_tracks['items']
        })

    @app.route("/api/spotify/user-saved-tracks")
    def user_saved_tracks():
        all_tracks = [] # List to hold all tracks
        sp, token_info, refresh_info = get_spotify_for_current_user() # Get the Spotify client
        saved_tracks = sp.current_user_saved_tracks(limit=20) # Get the first page of saved tracks
        tracks = [{"name": item["track"]["name"], 
                "artist": item["track"]["artists"][0]["name"], 
                "added_at": datetime.datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m.%d.%y"),
                "url": item["track"]["external_urls"]["spotify"]} 
                for item in saved_tracks["items"]]   
        return jsonify(tracks) # Return the list of all tracks

    # get current user currently playing track
    @app.route("/api/spotify/currently-playing")
    def currently_playing():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        current_playback = sp.current_playback(market="US", additional_types=['episode'])
        if current_playback and current_playback['is_playing']:
            return jsonify(current_playback)
        else:
            return jsonify({'message': 'nothing playing 🎵'})

    # Get user's top tracks
    @app.route("/api/spotify/top-tracks")
    def top_tracks():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        top_tracks = sp.current_user_top_tracks(limit=20)
        return jsonify(top_tracks)

    # Get user's recently played tracks
    @app.route("/api/spotify/recently-played")
    def recently_played():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        recently_played = sp.current_user_recently_played()
        return jsonify(recently_played)

    # Get user's saved tracks
    @app.route("/api/spotify/saved-tracks")
    def saved_tracks():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        saved_tracks = sp.current_user_saved_tracks(limit=20)
        return jsonify(saved_tracks)

    # Get user's playlists
    @app.route("/api/spotify/playlists")
    def playlists():
        sp, token_info, refresh_info = get_spotify_for_current_user()
        playlists = sp.current_user_playlists(limit=20)
        return jsonify(playlists)

    #Get playlist tracks
    @app.route("/api/spotify/playlist-tracks/<playlist_id>")
    def playlist_tracks(playlist_id):
        sp, token_info, refresh_info = get_spotify_for_current_user()
        playlist_tracks = sp.playlist_tracks(playlist_id)
        return jsonify(playlist_tracks)

    @app.route("/api/spotify/devices")
    def get_devices():
        sp, access_token, refresh_info = get_spotify_for_current_user()
        url = "https://api.spotify.com/v1/me/player/devices"
        headers = {
        "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if "devices" in data:
            for device in data["devices"]:
                print(f"Device Name: {device['name']}, ID: {device['id']}, Type: {device['type']}")
                return jsonify(data["devices"])
        else:
            print("No devices found. Make sure Spotify is open on a device.")
            return jsonify({"error": "No devices found"}), 404        

    @app.route("/api/spotify/u/<spotify_id>/top-tracks")
    def user_top_tracks(spotify_id):
        """Get top tracks for a specific user by their Spotify ID"""
        sp, access_token, refresh_token = get_spotify_by_user_id(spotify_id)
        if not sp:
            return jsonify({"error": "User not found or unable to access their data"}), 404
        
        try:
            top_tracks = sp.current_user_top_tracks(limit=20)
            return jsonify({
                "user_id": spotify_id,
                "top_tracks": top_tracks['items']
            })
        except Exception as e:
            return jsonify({"error": f"Failed to get top tracks: {str(e)}"}), 500

    @app.route("/api/spotify/u/<spotify_id>/top-artists")
    def user_top_artists(spotify_id):
        """Get top artists for a specific user by their Spotify ID"""
        sp, access_token, refresh_token = get_spotify_by_user_id(spotify_id)
        if not sp:
            return jsonify({"error": "User not found or unable to access their data"}), 404
        
        try:
            top_artists = sp.current_user_top_artists(limit=20)
            return jsonify({
                "user_id": spotify_id,
                "top_artists": top_artists['items']
            })
        except Exception as e:
            return jsonify({"error": f"Failed to get top artists: {str(e)}"}), 500

    @app.route("/api/spotify/u/<spotify_id>/playlists")
    def user_playlists(spotify_id):
        """Get playlists for a specific user by their Spotify ID"""
        sp, access_token, refresh_token = get_spotify_by_user_id(spotify_id)
        if not sp:
            return jsonify({"error": "User not found or unable to access their data"}), 404
        
        try:
            playlists = sp.current_user_playlists(limit=20)
            return jsonify({
                "user_id": spotify_id,
                "playlists": playlists['items']
            })
        except Exception as e:
            return jsonify({"error": f"Failed to get playlists: {str(e)}"}), 500

    @app.route("/api/spotify/u/<spotify_id>/currently-playing")
    def user_currently_playing(spotify_id):
        """Get currently playing track for a specific user by their Spotify ID"""
        sp, access_token, refresh_token = get_spotify_by_user_id(spotify_id)
        if not sp:
            return jsonify({"error": "User not found or unable to access their data"}), 404
        
        try:
            current_playback = sp.current_playback(market="US", additional_types=['episode'])
            if current_playback and current_playback['is_playing']:
                return jsonify({
                    "user_id": spotify_id,
                    "currently_playing": current_playback
                })
            else:
                return jsonify({
                    "user_id": spotify_id,
                    "message": "nothing playing 🎵"
                })
        except Exception as e:
            return jsonify({"error": f"Failed to get currently playing: {str(e)}"}), 500