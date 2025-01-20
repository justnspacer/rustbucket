import datetime
from flask import Flask, request, redirect, session, jsonify, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.secret_key = "thisisasecret"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPE = "user-top-read user-read-recently-played user-library-read ugc-image-upload streaming playlist-read-private"

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
    
@app.route("/")
def home():
    token_info = cache_handler.get_cached_token()
    sp = spotipy.Spotify(auth=token_info.get("access_token"))

    if not token_info:
        return render_template("index.html", token_info=None)
    
    sp = spotipy.Spotify(auth=token_info.get("access_token"))
    user = sp.current_user()
    # Check if the token has expired
    now = datetime.now()
    expires_at = datetime.fromtimestamp(token_info['expires_at'])
    if now >= expires_at:
        # Refresh the token
        refresh_token = token_info['refresh_token']
        new_access_token = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
        token_info['access_token'] = new_access_token
        token_info['expires_at'] = (now + datetime.timedelta(seconds=3600)).timestamp()  # Assuming the new token is valid for 1 hour
        cache_handler.save_token_to_cache(token_info)    
    user = spotipy.Spotify(auth=token_info).current_user()
    return render_template("index.html", token_info=token_info, user=user)

@app.route("/login")
def login():
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/request-token")
def request_token():
    code = request.args.get("code")
    token_info = cache_handler.save_token_to_cache(code)
    return jsonify(token_info)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = cache_handler.save_token_to_cache(code)
    session["token_info"] = token_info
    return jsonify(token_info)

@app.route("/currently-playing")
def currently_playing():
    token_info = cache_handler.get_cached_token()
    sp = spotipy.Spotify(auth=token_info.get("access_token"))
    current_track = sp.currently_playing()
    return jsonify(current_track)

if __name__ == "__main__":
    app.run(debug=True)