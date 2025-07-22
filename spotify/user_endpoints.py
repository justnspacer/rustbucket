from flask import jsonify, request, render_template
from datetime import datetime
from .spotify_client import get_spotify_by_user_id, get_user_info_by_id
from .supabase_helpers import get_spotify_id_for_supabase_user, search_users_supabase, get_user_from_supabase, save_or_update_user_supabase
from .auth import require_authenticated_user

def register_user_endpoints(app):
    """Register all user-related endpoints"""
    
    @app.route("/spotify/u/<spotify_id>")
    def public_profile(spotify_id):
        """Public profile for a Spotify user"""
        user_data = get_user_info_by_id(spotify_id)
        if not user_data:
            return jsonify({"error": "User not found or hasn't authorized this app"}), 404
        
        # Handle both fresh Spotify data and cached Supabase data
        if 'id' in user_data:  # Fresh Spotify data
            public_data = {
                'spotify_id': user_data.get('id', spotify_id),
                'followers': user_data.get('followers', {}).get('total', 0) if isinstance(user_data.get('followers'), dict) else user_data.get('followers', 0),
                'images': user_data.get('images', []),
                'country': user_data.get('country'),
                'product': user_data.get('product'),
                'external_urls': user_data.get('external_urls', {}),
                'last_updated': datetime.now().isoformat()
            }
        else:  # Cached Supabase data
            public_data = {
                'spotify_id': user_data['spotify_id'],
                'followers': user_data.get('followers', 0),
                'images': user_data.get('images', []),
                'country': user_data.get('country'),
                'product': user_data.get('product'),
                'external_urls': user_data.get('external_urls', {}),
                'last_updated': user_data.get('last_updated')
            }
        
        return render_template("user_profile.html", user=public_data, is_public=True)

    @app.route("/spotify/search-users")
    def search_users():
        """Search for users who have authorized the app"""
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 20))
        
        users = search_users_supabase(query, limit)
        
        public_users = [{
            'spotify_id': user['spotify_id'],
            'followers': user.get('followers', 0),
            'images': user.get('images', []),
            'country': user.get('country'),
            'product': user.get('product'),
            'last_updated': user.get('last_updated')
        } for user in users]
        
        return jsonify({
            'users': public_users,
            'total': len(public_users),
            'query': query
        })

    @app.route("/spotify/users")
    def list_users():
        """List all users who have authorized the app"""
        limit = int(request.args.get('limit', 20))
        users = search_users_supabase(limit=limit)
        
        public_users = [{
            'spotify_id': user['spotify_id'],
            'followers': user.get('followers', 0),
            'images': user.get('images', []),
            'country': user.get('country'),
            'product': user.get('product'),
            'last_updated': user.get('last_updated')
        } for user in users]
        
        return jsonify({
            'users': public_users,
            'total': len(public_users)
        })

    # User-specific Spotify data endpoints
    @app.route("/spotify/u/<spotify_id>/top-tracks")
    def user_top_tracks(spotify_id):
        """Get top tracks for a specific user"""
        sp, _, _ = get_spotify_by_user_id(spotify_id)
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

    @app.route("/spotify/u/<spotify_id>/top-artists")
    def user_top_artists(spotify_id):
        """Get top artists for a specific user"""
        sp, _, _ = get_spotify_by_user_id(spotify_id)
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

    @app.route("/spotify/u/<spotify_id>/playlists")
    def user_playlists(spotify_id):
        """Get playlists for a specific user"""
        sp, _, _ = get_spotify_by_user_id(spotify_id)
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

    @app.route("/spotify/u/<spotify_id>/currently-playing")
    def user_currently_playing(spotify_id):
        """Get currently playing track for a specific user"""
        sp, _, _ = get_spotify_by_user_id(spotify_id)
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

    # Authenticated user endpoints
    @app.route("/spotify/auth/profile")
    @require_authenticated_user
    def auth_profile(user):
        """Get profile for authenticated user"""
        spotify_id = get_spotify_id_for_supabase_user(user['id'])
        if not spotify_id:
            return jsonify({
                "error": "Spotify account not linked",
                "supabase_user": user,
                "link_spotify_url": "/spotify/auth/link"
            }), 404
        
        user_data = get_user_info_by_id(spotify_id)
        if not user_data:
            return jsonify({"error": "Spotify user data not found"}), 404
            
        return jsonify({
            "supabase_user": user,
            "spotify_data": user_data
        })

    @app.route("/spotify/auth/link", methods=["POST"])
    @require_authenticated_user
    def auth_link_spotify(user):
        """Link authenticated user to Spotify account"""
        data = request.get_json()
        spotify_id = data.get('spotify_id')
        
        if not spotify_id:
            return jsonify({"error": "spotify_id required"}), 400
        
        spotify_user = get_user_from_supabase(spotify_id)
        if not spotify_user:
            return jsonify({"error": "Spotify user not found. Please authorize with Spotify first."}), 404
        
        result = save_or_update_user_supabase(spotify_id, user['id'])
        if result:
            return jsonify({
                "message": "Successfully linked Spotify account",
                "supabase_user_id": user['id'],
                "spotify_id": spotify_id
            })
        else:
            return jsonify({"error": "Failed to link accounts"}), 500

    @app.route("/spotify/auth/top-tracks")
    @require_authenticated_user
    def auth_top_tracks(user):
        """Get top tracks for authenticated user"""
        return _auth_spotify_data(user, 'current_user_top_tracks', 'top_tracks')

    @app.route("/spotify/auth/playlists")
    @require_authenticated_user
    def auth_playlists(user):
        """Get playlists for authenticated user"""
        return _auth_spotify_data(user, 'current_user_playlists', 'playlists')

    @app.route("/spotify/auth/currently-playing")
    @require_authenticated_user
    def auth_currently_playing(user):
        """Get currently playing track for authenticated user"""
        spotify_id = get_spotify_id_for_supabase_user(user['id'])
        if not spotify_id:
            return jsonify({"error": "Spotify account not linked"}), 404
        
        sp, _, _ = get_spotify_by_user_id(spotify_id)
        if not sp:
            return jsonify({"error": "Unable to access Spotify data"}), 404
        
        try:
            current_playback = sp.current_playback(market="US", additional_types=['episode'])
            if current_playback and current_playback['is_playing']:
                return jsonify({
                    "supabase_user_id": user['id'],
                    "spotify_id": spotify_id,
                    "currently_playing": current_playback
                })
            else:
                return jsonify({
                    "supabase_user_id": user['id'],
                    "spotify_id": spotify_id,
                    "message": "nothing playing 🎵"
                })
        except Exception as e:
            return jsonify({"error": f"Failed to get currently playing: {str(e)}"}), 500

def _auth_spotify_data(user, method_name, data_key):
    """Helper function for authenticated Spotify data endpoints"""
    spotify_id = get_spotify_id_for_supabase_user(user['id'])
    if not spotify_id:
        return jsonify({"error": "Spotify account not linked"}), 404
    
    sp, _, _ = get_spotify_by_user_id(spotify_id)
    if not sp:
        return jsonify({"error": "Unable to access Spotify data"}), 404
    
    try:
        method = getattr(sp, method_name)
        data = method(limit=20)
        return jsonify({
            "supabase_user_id": user['id'],
            "spotify_id": spotify_id,
            data_key: data['items']
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get {data_key}: {str(e)}"}), 500