import datetime
from flask import Flask, request, redirect, session, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import os
import requests
import time



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
    current_playback = sp.current_playback(market="US", additional_types=['episode'])
    if current_playback and current_playback['is_playing']:
        return jsonify(current_playback)
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

def pause_track(track_uri):
    sp, access_token = get_spotify()
    url = "https://api.spotify.com/v1/me/player/pause"
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


def next_track(track_uri):
    sp, access_token = get_spotify()
    url = "https://api.spotify.com/v1/me/player/next"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "uris": [track_uri],
        "device_id": DEVICE_ID
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def previous_track(track_uri):
    sp, access_token = get_spotify()
    url = "https://api.spotify.com/v1/me/player/previous"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "uris": [track_uri],
        "device_id": DEVICE_ID
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def seek(track_uri, position_in_milliseconds):
    sp, access_token = get_spotify()
    url = f"https://api.spotify.com/v1/me/player/seek?position_ms={position_in_milliseconds}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers)
    return response.json()

def volume(track_uri, control):
    sp, access_token = get_spotify()
    url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={control}"
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

def repeat(track_uri, state):
    sp, access_token = get_spotify()
    url = f"https://api.spotify.com/v1/me/player/repeat?state={state}"
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

def shuffle(track_uri, state):
    sp, access_token = get_spotify()
    url = f"https://api.spotify.com/v1/me/player/shuffle?state={state}"
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

def get_audio_features(track_id):
    sp, access_token = get_spotify()
    return sp.audio_features([track_id])[0]

def get_audio_analysis(track_id):
    sp, access_token = get_spotify()
    return sp._get(f"audio-analysis/{track_id}")

def control_visual_effects(playback_position, audio_analysis):
    # Example: Trigger an effect if the current time matches a beat timestamp
    beats = audio_analysis.get('beats', [])
    for beat in beats:
        beat_time = beat['start'] * 1000  # converting seconds to milliseconds
        if abs(beat_time - playback_position) < 50:  # 50ms tolerance
            trigger_visual_effect()

def trigger_visual_effect():
    # Implement your visual effect logic here
    print("Visual effect triggered!")
    while True:
        # Get current playback info
        sp, access_token = get_spotify()
        current_playback = sp.current_playback()
        if current_playback and current_playback['item']:
            track_id = current_playback['item']['id']
            playback_position = current_playback['progress_ms']
            
            # Retrieve analysis data if not already fetched or if track changed
            audio_analysis = get_audio_analysis(track_id)
            
            # Call your function to control visuals based on playback position
            control_visual_effects(playback_position, audio_analysis)
            
        time.sleep(0.05)  # Check 20 times per second for near real-time updates


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


@app.route('/next', methods=['POST'])
def next():
    data = request.json
    track_uri = data.get("track_uri")

    if not track_uri:
        return jsonify({"error": "No track URI provided"}), 400
    
    response = next_track(track_uri)
    return jsonify(response)

@app.route('/previous', methods=['POST'])
def previous():
    data = request.json
    track_uri = data.get("track_uri")

    if not track_uri:
        return jsonify({"error": "No track URI provided"}), 400
    
    response = previous_track(track_uri)
    return jsonify(response)

@app.route('/seek', methods=['PUT'])
def seek_position():
    data = request.json
    track_uri = data.get("track_uri")
    position_ms = data.get("position_ms")

    if not track_uri or position_ms is None:
        return jsonify({"error": "Track URI and position in milliseconds must be provided"}), 400

    response = seek(track_uri, position_ms)
    return jsonify(response)

@app.route('/volume', methods=['PUT'])
def set_volume():
    data = request.json
    track_uri = data.get("track_uri")
    volume_percent = data.get("volume_percent")

    if not track_uri or volume_percent is None:
        return jsonify({"error": "Track URI and volume percent must be provided"}), 400

    response = volume(track_uri, volume_percent)
    return jsonify(response)

@app.route('/repeat', methods=['PUT'])
def set_repeat():
    data = request.json
    track_uri = data.get("track_uri")
    state = data.get("state")

    if not track_uri or state is None:
        return jsonify({"error": "Track URI and repeat state must be provided"}), 400

    response = repeat(track_uri, state)
    return jsonify(response)

@app.route('/shuffle', methods=['PUT'])
def set_shuffle():
    data = request.json
    track_uri = data.get("track_uri")
    state = data.get("state")

    if not track_uri or state is None:
        return jsonify({"error": "Track URI and shuffle state must be provided"}), 400

    response = shuffle(track_uri, state)
    return jsonify(response)


@app.route('/pause', methods=['PUT'])
def pause():
    data = request.json
    track_uri = data.get("track_uri")

    if not track_uri:
        return jsonify({"error": "No track URI provided"}), 400
    
    response = pause_track(track_uri)
    return jsonify(response)



if __name__ == "__main__":
    app.run(debug=True)