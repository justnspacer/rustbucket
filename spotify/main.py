from flask import Flask, request, redirect, session, jsonify
import spotify
from spotify.oauth import OAuth2
from dotenv import load_dotenv
import os
import redis

load_dotenv()


app = Flask(__name__)

app.secret_key = "thisisasecret"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SCOPES = "user-top-read"

# user-read-recently-played user-library-read ugc-image-upload streaming playlist-read-private

oauth2 = OAuth2(client_id=CLIENT_ID,
                        redirect_uri=REDIRECT_URI, 
                        scopes=SCOPES)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def store_token_in_redis(token, expires_in):
    redis_client.setex('spotify_token', expires_in, token)

def get_token_from_redis():
    return redis_client.get('spotify_token').decode('utf-8')

@app.route("/")
def login():
    auth_url = oauth2.url
    return redirect(auth_url)

@app.route("/request-token")
def request_token():
    code = request.args.get("code")
    token_info = oauth2.get_access_token(code)
    return jsonify(token_info)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = oauth2.get_access_token(code)
    session["token_info"] = token_info
    return jsonify(token_info)

@app.route("/currently-playing")
def currently_playing():
    token_info = session.get("token_info", {})
    sp = spotify.Spotify(auth=token_info.get("access_token"))
    current_track = sp.currently_playing()
    return jsonify(current_track)

if __name__ == "__main__":
    app.run(debug=True)