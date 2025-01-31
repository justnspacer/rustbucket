import datetime
from flask import Flask, request, redirect, session, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import os
import requests


load_dotenv()


app = Flask(__name__)

app.secret_key = "thisisasecret"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
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
    return sp, token_info["access_token"]


@app.route("/")
def home():
    sp, token_info = get_spotify()
    return render_template("index.html", user=sp.current_user(), token_info=token_info)

@app.route("/login")
def login():
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/request-token")
def request_token():
    code = request.args.get("code")
    token_info = oauth.get_access_token(code)
    return jsonify(token_info)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = oauth.get_access_token(code)
    session["token_info"] = token_info
    return jsonify(token_info)


# get current user currently playing track
@app.route("/currently-playing")
def currently_playing():
    sp, token_info = get_spotify()
    current_playback = sp.current_playback()
    if current_playback and current_playback['is_playing']:
        item = current_playback['item']
        if current_playback['currently_playing_type'] == 'track':
            track_info = {
                'type': 'track',
                'name': item['name'],
                'album': item['album']['name'],
                'artists': [artist['name'] for artist in item['artists']],
                'images': item['album']['images'],
                'spotify_uri': item['uri']
            }
            return jsonify(track_info)
        elif current_playback['currently_playing_type'] == 'episode':
            episode_info = {
                'type': 'episode',
                'name': 'Listening to a podcast',
                'album': 'New episode',
                'artists': ['cool podcasters'],
                'images': [ {'url':'https://images.unsplash.com/photo-1737071371043-761e02b1ef95?q=80&w=1319&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}]
            }
            return jsonify(episode_info)
    else:
        return jsonify({'message': '🛑🎵'})

# Get user's top tracks
@app.route("/top-tracks")
def top_tracks():
    sp, token_info = get_spotify()
    top_tracks = sp.current_user_top_tracks()
    return jsonify(top_tracks)

# Get user's recently played tracks
@app.route("/recently-played")
def recently_played():
    sp, token_info = get_spotify()
    recently_played = sp.current_user_recently_played()
    return jsonify(recently_played)

# Get user's saved tracks
@app.route("/saved-tracks")
def saved_tracks():
    sp, token_info = get_spotify()
    saved_tracks = sp.current_user_saved_tracks()
    return jsonify(saved_tracks)

# Get user's playlists
@app.route("/playlists")
def playlists():
    sp, token_info = get_spotify()
    playlists = sp.current_user_playlists()
    return jsonify(playlists)

def play_track(track_uri):
    sp, access_token = get_spotify()
    url = "https://api.spotify.com/v1/me/player/play"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "uris": [track_uri],
        "device_id": DEVICE_ID
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

@app.route("/devices")
def get_devices():
    sp, access_token = get_spotify()
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

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    track_uri = data.get("track_uri")

    if not track_uri:
        return jsonify({"error": "No track URI provided"}), 400
    
    response = play_track(track_uri)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)