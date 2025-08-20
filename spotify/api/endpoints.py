"""
Spotify API endpoints for user data retrieval
"""
import spotipy
import base64
from flask import request
from .auth import require_spotify_auth
from .helpers import success_response, error_response, paginated_response
from .database import get_user_by_spotify_id
from .errors import *

def register_spotify_routes(app):
    """Register all Spotify API routes"""
    
    # Profile endpoints
    @app.route("/api/spotify/profile/<spotify_id>")
    def spotify_profile(spotify_id):
        """Get Spotify user profile by spotify_id"""
        spotify_user = get_user_by_spotify_id(spotify_id)
        if not spotify_user:
            return error_response(
                message="Spotify user not found", 
                status_code=404, 
                error_code=NOT_FOUND
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            profile = sp.user(spotify_id)
            
            return success_response(
                data=profile,
                message="Profile retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve profile", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/profile/<spotify_id>/playlists")
    def spotify_user_playlists(spotify_id):
        """Get user's playlists by spotify_id"""
        spotify_user = get_user_by_spotify_id(spotify_id)
        if not spotify_user:
            return error_response(
                message="Spotify user not found", 
                status_code=404, 
                error_code=NOT_FOUND
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            playlists = sp.user_playlists(spotify_id, limit=limit, offset=offset)
            
            return success_response(
                data=playlists,
                message="Playlists retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve playlists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/profile/<spotify_id>/top-tracks")
    def spotify_user_top_tracks(spotify_id):
        """Get user's top tracks by spotify_id"""
        spotify_user = get_user_by_spotify_id(spotify_id)
        if not spotify_user:
            return error_response(
                message="Spotify user not found", 
                status_code=404, 
                error_code=NOT_FOUND
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            
            time_range = request.args.get('time_range', 'medium_term')
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            top_tracks = sp.current_user_top_tracks(
                time_range=time_range, 
                limit=limit, 
                offset=offset
            )
            
            return success_response(
                data=top_tracks,
                message="Top tracks retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve top tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/profile/<spotify_id>/top-artists")
    def spotify_user_top_artists(spotify_id):
        """Get user's top artists by spotify_id"""
        spotify_user = get_user_by_spotify_id(spotify_id)
        if not spotify_user:
            return error_response(
                message="Spotify user not found", 
                status_code=404, 
                error_code=NOT_FOUND
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            
            time_range = request.args.get('time_range', 'medium_term')
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            top_artists = sp.current_user_top_artists(
                time_range=time_range, 
                limit=limit, 
                offset=offset
            )
            
            return success_response(
                data=top_artists,
                message="Top artists retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve top artists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    # Current user endpoints (require authentication)
    @app.route("/api/spotify/my/profile")
    @require_spotify_auth
    def my_spotify_profile():
        """Get current user's Spotify profile"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            profile = sp.current_user()
            
            return success_response(
                data=profile,
                message="Profile retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve profile", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/playlists")
    @require_spotify_auth
    def my_spotify_playlists():
        """Get current user's playlists"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            playlists = sp.current_user_playlists(limit=limit, offset=offset)
            
            return success_response(
                data=playlists,
                message="Playlists retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve playlists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/saved-tracks")
    @require_spotify_auth
    def my_saved_tracks():
        """Get current user's saved tracks"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            saved_tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
            
            return success_response(
                data=saved_tracks,
                message="Saved tracks retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve saved tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/top-tracks")
    @require_spotify_auth
    def my_top_tracks():
        """Get current user's top tracks"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            time_range = request.args.get('time_range', 'medium_term')
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            top_tracks = sp.current_user_top_tracks(
                time_range=time_range, 
                limit=limit, 
                offset=offset
            )
            
            return success_response(
                data=top_tracks,
                message="Top tracks retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve top tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/top-artists")
    @require_spotify_auth
    def my_top_artists():
        """Get current user's top artists"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            time_range = request.args.get('time_range', 'medium_term')
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            top_artists = sp.current_user_top_artists(
                time_range=time_range, 
                limit=limit, 
                offset=offset
            )
            
            return success_response(
                data=top_artists,
                message="Top artists retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve top artists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/recently-played")
    @require_spotify_auth
    def my_recently_played():
        """Get current user's recently played tracks"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            limit = min(int(request.args.get('limit', 20)), 50)
            before = request.args.get('before')
            after = request.args.get('after')
            
            kwargs = {'limit': limit}
            if before:
                kwargs['before'] = before
            if after:
                kwargs['after'] = after
            
            recently_played = sp.current_user_recently_played(**kwargs)
            
            return success_response(
                data=recently_played,
                message="Recently played tracks retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve recently played tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/my/following")
    @require_spotify_auth
    def my_following():
        """Get artists/users that current user follows"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            follow_type = request.args.get('type', 'artist')  # artist or user
            limit = min(int(request.args.get('limit', 20)), 50)
            after = request.args.get('after')
            
            kwargs = {'type': follow_type, 'limit': limit}
            if after:
                kwargs['after'] = after
            
            following = sp.current_user_following_artists(**kwargs) if follow_type == 'artist' else sp.current_user_followed_artists(**kwargs)
            
            return success_response(
                data=following,
                message="Following retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve following", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    # Playlist endpoints
    @app.route("/api/spotify/playlists/<playlist_id>")
    def get_playlist(playlist_id):
        """Get playlist details"""
        # Get user authentication for token access
        user_id = request.headers.get('x-user-id')
        if not user_id:
            return error_response(
                message="User authentication required", 
                status_code=401, 
                error_code=AUTH_REQUIRED
            )
        
        from .database import get_user_by_supabase_id
        spotify_user = get_user_by_supabase_id(user_id)
        if not spotify_user:
            return error_response(
                message="Spotify authorization required", 
                status_code=403, 
                error_code=SPOTIFY_UNAUTHORIZED
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            
            playlist = sp.playlist(playlist_id)
            
            return success_response(
                data=playlist,
                message="Playlist retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve playlist", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/playlists/<playlist_id>/tracks")
    def get_playlist_tracks(playlist_id):
        """Get tracks from a playlist"""
        # Get user authentication for token access
        user_id = request.headers.get('x-user-id')
        if not user_id:
            return error_response(
                message="User authentication required", 
                status_code=401, 
                error_code=AUTH_REQUIRED
            )
        
        from .database import get_user_by_supabase_id
        spotify_user = get_user_by_supabase_id(user_id)
        if not spotify_user:
            return error_response(
                message="Spotify authorization required", 
                status_code=403, 
                error_code=SPOTIFY_UNAUTHORIZED
            )
        
        try:
            access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
            sp = spotipy.Spotify(auth=access_token)
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            tracks = sp.playlist_tracks(playlist_id, limit=limit, offset=offset)
            
            return success_response(
                data=tracks,
                message="Playlist tracks retrieved successfully"
            )
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to retrieve playlist tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    # Search endpoints
    @app.route("/api/spotify/search/users")
    def search_users():
        """Search for users who have linked Spotify accounts"""
        try:
            from .database import get_supabase_client
            
            query = request.args.get('q', '').strip()
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            
            supabase = get_supabase_client()
            
            if query:
                # Search by spotify_id (partial match)
                result = supabase.table('app_spotify').select(
                    'user_id, spotify_id, linked_at, created_at'
                ).ilike('spotify_id', f'%{query}%').range(offset, offset + limit - 1).execute()
            else:
                # Get all users (for browse/discovery)
                result = supabase.table('app_spotify').select(
                    'user_id, spotify_id, linked_at, created_at'
                ).range(offset, offset + limit - 1).execute()
            
            users = []
            for user in result.data:
                # Get basic Spotify profile for each user
                try:
                    access_token = base64.urlsafe_b64decode(
                        supabase.table('app_spotify').select('encrypted_access_token')
                        .eq('user_id', user['user_id']).execute().data[0]['encrypted_access_token'] + '=='
                    ).decode('utf-8')
                    
                    sp = spotipy.Spotify(auth=access_token)
                    profile = sp.user(user['spotify_id'])
                    
                    users.append({
                        'user_id': user['user_id'],
                        'spotify_id': user['spotify_id'],
                        'display_name': profile.get('display_name') or user['spotify_id'],
                        'images': profile.get('images', []),
                        'followers': profile.get('followers', {}).get('total', 0),
                        'linked_at': user.get('linked_at'),
                        'profile_url': profile.get('external_urls', {}).get('spotify')
                    })
                except Exception as e:
                    # If we can't get profile, still include basic info
                    print(f"Error getting profile for {user['spotify_id']}: {e}")
                    users.append({
                        'user_id': user['user_id'],
                        'spotify_id': user['spotify_id'],
                        'display_name': user['spotify_id'],
                        'images': [],
                        'followers': 0,
                        'linked_at': user.get('linked_at'),
                        'profile_url': None
                    })
            
            return success_response(
                data={
                    'users': users,
                    'pagination': {
                        'limit': limit,
                        'offset': offset,
                        'total': len(users)
                    }
                },
                message="Users retrieved successfully"
            )
            
        except Exception as e:
            return error_response(
                message="Failed to search users", 
                status_code=500, 
                error_code=INTERNAL_ERROR,
                details={'error': str(e)}
            )

    @app.route("/api/spotify/search")
    @require_spotify_auth
    def search_spotify():
        """Search Spotify catalog for tracks, artists, albums, playlists"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            query = request.args.get('q', '').strip()
            if not query:
                return error_response(
                    message="Search query is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            search_type = request.args.get('type', 'track,artist,album,playlist')
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            market = request.args.get('market', 'US')
            
            # Perform search
            results = sp.search(
                q=query,
                type=search_type,
                limit=limit,
                offset=offset,
                market=market
            )
            
            return success_response(
                data=results,
                message="Search completed successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to perform search", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/search/tracks")
    @require_spotify_auth
    def search_tracks():
        """Search for tracks specifically"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            query = request.args.get('q', '').strip()
            if not query:
                return error_response(
                    message="Search query is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            market = request.args.get('market', 'US')
            
            results = sp.search(
                q=query,
                type='track',
                limit=limit,
                offset=offset,
                market=market
            )
            
            return success_response(
                data=results['tracks'],
                message="Track search completed successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to search tracks", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/search/artists")
    @require_spotify_auth
    def search_artists():
        """Search for artists specifically"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            query = request.args.get('q', '').strip()
            if not query:
                return error_response(
                    message="Search query is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            market = request.args.get('market', 'US')
            
            results = sp.search(
                q=query,
                type='artist',
                limit=limit,
                offset=offset,
                market=market
            )
            
            return success_response(
                data=results['artists'],
                message="Artist search completed successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to search artists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/search/albums")
    @require_spotify_auth
    def search_albums():
        """Search for albums specifically"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            query = request.args.get('q', '').strip()
            if not query:
                return error_response(
                    message="Search query is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            market = request.args.get('market', 'US')
            
            results = sp.search(
                q=query,
                type='album',
                limit=limit,
                offset=offset,
                market=market
            )
            
            return success_response(
                data=results['albums'],
                message="Album search completed successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to search albums", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/search/playlists")
    @require_spotify_auth
    def search_playlists():
        """Search for playlists specifically"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            query = request.args.get('q', '').strip()
            if not query:
                return error_response(
                    message="Search query is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            limit = min(int(request.args.get('limit', 20)), 50)
            offset = int(request.args.get('offset', 0))
            market = request.args.get('market', 'US')
            
            results = sp.search(
                q=query,
                type='playlist',
                limit=limit,
                offset=offset,
                market=market
            )
            
            return success_response(
                data=results['playlists'],
                message="Playlist search completed successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to search playlists", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    # Recommendations endpoint
    @app.route("/api/spotify/recommendations")
    @require_spotify_auth
    def get_recommendations():
        """Get music recommendations based on seed tracks/artists/genres"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            # Get seed parameters
            seed_tracks = request.args.getlist('seed_tracks[]') or request.args.get('seed_tracks', '').split(',')
            seed_artists = request.args.getlist('seed_artists[]') or request.args.get('seed_artists', '').split(',')
            seed_genres = request.args.getlist('seed_genres[]') or request.args.get('seed_genres', '').split(',')
            
            # Filter out empty values
            seed_tracks = [t for t in seed_tracks if t.strip()]
            seed_artists = [a for a in seed_artists if a.strip()]
            seed_genres = [g for g in seed_genres if g.strip()]
            
            # Spotify requires at least one seed
            if not any([seed_tracks, seed_artists, seed_genres]):
                return error_response(
                    message="At least one seed (track, artist, or genre) is required", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            limit = min(int(request.args.get('limit', 20)), 100)
            market = request.args.get('market', 'US')
            
            # Optional audio features for recommendations
            kwargs = {'limit': limit, 'market': market}
            
            if seed_tracks:
                kwargs['seed_tracks'] = seed_tracks[:5]  # Max 5 seeds
            if seed_artists:
                kwargs['seed_artists'] = seed_artists[:5]
            if seed_genres:
                kwargs['seed_genres'] = seed_genres[:5]
            
            # Audio feature parameters (optional)
            audio_features = [
                'acousticness', 'danceability', 'energy', 'instrumentalness', 
                'liveness', 'loudness', 'speechiness', 'tempo', 'valence'
            ]
            
            for feature in audio_features:
                target_val = request.args.get(f'target_{feature}')
                min_val = request.args.get(f'min_{feature}')
                max_val = request.args.get(f'max_{feature}')
                
                if target_val:
                    kwargs[f'target_{feature}'] = float(target_val)
                if min_val:
                    kwargs[f'min_{feature}'] = float(min_val)
                if max_val:
                    kwargs[f'max_{feature}'] = float(max_val)
            
            recommendations = sp.recommendations(**kwargs)
            
            return success_response(
                data=recommendations,
                message="Recommendations retrieved successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to get recommendations", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

    @app.route("/api/spotify/genres")
    @require_spotify_auth  
    def get_available_genres():
        """Get available genre seeds for recommendations"""
        try:
            sp = spotipy.Spotify(auth=request.spotify_token)
            
            genres = sp.recommendation_genre_seeds()
            
            return success_response(
                data=genres,
                message="Available genres retrieved successfully"
            )
            
        except spotipy.SpotifyException as e:
            return error_response(
                message=f"Spotify API error: {str(e)}", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )
        except Exception as e:
            return error_response(
                message="Failed to get available genres", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )
