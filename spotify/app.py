import datetime
from flask import Flask, request, redirect, session, jsonify, render_template, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import requests, os
from models import User
from flask_sqlalchemy import SQLAlchemy
from extensions import db, migrate


load_dotenv()

def save_or_update_user(spotify_id, display_name, access_token, refresh_token):
    user = User.query.filter_by(spotify_id=spotify_id).first()
    if user:
        user.display_name = display_name
        user.access_token = access_token
        user.refresh_token = refresh_token
    else:
        user = User(
            spotify_id=spotify_id,
            display_name=display_name,
            access_token=access_token,
            refresh_token=refresh_token
        )
        db.session.add(user)
    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.secret_key = "thisisasecret"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI = "http://127.0.0.1:5000/spotify/callback"
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    SCOPE = "user-top-read user-read-recently-played user-read-currently-playing user-library-read ugc-image-upload streaming playlist-read-private streaming user-read-private user-read-email user-modify-playback-state user-read-playback-state"
    DEVICE_ID = "your_device_id"

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

        response = request.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception('Failed to refresh token')

    def get_spotify():
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

    @app.route("/spotify")
    def home():
        sp, token_info, refresh_info = get_spotify()
        return render_template("index.html", user=sp.current_user(), token_info=token_info)

    @app.route("/spotify/u/<spotify_id>")
    def public_profile(spotify_id):
        sp, token_info, refresh_info = get_spotify()
        user_info = sp.current_user()
        user = User.query.filter_by(spotify_id=user_info['id']).first()
        if not user:
            user = User(spotify_id=user_info['id'])
        user.display_name = user_info['display_name']
        user.access_token = token_info
        user.refresh_token = token_info
        db.session.add(user)
        db.session.commit()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return render_template("user_profile.html", user=sp.current_user(), token_info=token_info)

    @app.route("/spotify/login")
    def login():
        auth_url = oauth.get_authorize_url()
        return redirect(auth_url)

    @app.route("/spotify/request-token")
    def request_token():
        code = request.args.get("code")
        token_info = oauth.get_access_token(code)
        return jsonify(token_info)

    @app.route("/spotify/callback")
    def callback():
        code = request.args.get("code")
        token_info = oauth.get_access_token(code)
        session["token_info"] = token_info
        return jsonify(token_info)

    @app.route("/spotify/top-artists-and-tracks")
    def top_artists_and_tracks():
        sp, token_info, refresh_info = get_spotify()
        top_artists = sp.current_user_top_artists(limit=20)
        top_tracks = sp.current_user_top_tracks(limit=20)
        return jsonify({
            "top_artists": top_artists['items'],
            "top_tracks": top_tracks['items']
        })

    @app.route("/spotify/user-saved-tracks")
    def user_saved_tracks():
        all_tracks = [] # List to hold all tracks
        sp, token_info, refresh_info = get_spotify() # Get the Spotify client
        saved_tracks = sp.current_user_saved_tracks(limit=20) # Get the first page of saved tracks
        tracks = [{"name": item["track"]["name"], 
                "artist": item["track"]["artists"][0]["name"], 
                "added_at": datetime.datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m.%d.%y"),
                "url": item["track"]["external_urls"]["spotify"]} 
                for item in saved_tracks["items"]]
        # while saved_tracks: # Loop through all pages of saved tracks
        #     # Extract relevant information from each track
        #     tracks = [{"name": item["track"]["name"], 
        #            "artist": item["track"]["artists"][0]["name"], 
        #            "added_at": datetime.datetime.strptime(item["added_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%m/%d/%Y"),
        #            "url": item["track"]["external_urls"]["spotify"]} 
        #           for item in saved_tracks["items"]]
        #     all_tracks.extend(tracks) # Add the tracks to the list
        #     saved_tracks = sp.next(saved_tracks) # Get the next page of tracks        
        return jsonify(tracks) # Return the list of all tracks

    # get current user currently playing track
    @app.route("/spotify/currently-playing")
    def currently_playing():
        sp, token_info, refresh_info = get_spotify()
        current_playback = sp.current_playback(market="US", additional_types=['episode'])
        if current_playback and current_playback['is_playing']:
            return jsonify(current_playback)
        else:
            return jsonify({'message': 'nothing playing 🎵'})

    # Get user's top tracks
    @app.route("/spotify/top-tracks")
    def top_tracks():
        sp, token_info, refresh_info = get_spotify()
        top_tracks = sp.current_user_top_tracks(limit=20)
        return jsonify(top_tracks)

    # Get user's recently played tracks
    @app.route("/spotify/recently-played")
    def recently_played():
        sp, token_info, refresh_info = get_spotify()
        recently_played = sp.current_user_recently_played()
        return jsonify(recently_played)

    # Get user's saved tracks
    @app.route("/spotify/saved-tracks")
    def saved_tracks():
        sp, token_info, refresh_info = get_spotify()
        saved_tracks = sp.current_user_saved_tracks(limit=20)
        return jsonify(saved_tracks)

    # Get user's playlists
    @app.route("/spotify/playlists")
    def playlists():
        sp, token_info, refresh_info = get_spotify()
        playlists = sp.current_user_playlists(limit=20)
        return jsonify(playlists)

    #Get playlist tracks
    @app.route("/spotify/playlist-tracks/<playlist_id>")
    def playlist_tracks(playlist_id):
        sp, token_info, refresh_info = get_spotify()
        playlist_tracks = sp.playlist_tracks(playlist_id)
        return jsonify(playlist_tracks)

    @app.route("/spotify/devices")
    def get_devices():
        sp, access_token, refresh_info = get_spotify()
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

    @app.route('/save_user')
    def save_user():
        sp, token_info, refresh_info = get_spotify()
        save_or_update_user(sp.current_user()["id"], sp.current_user()["display_name"], token_info, refresh_info)
        return f"User {sp.current_user()["display_name"]} saved!"

    return app