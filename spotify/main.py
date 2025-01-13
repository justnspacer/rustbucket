from flask import Flask, request, redirect, session, jsonify
import spotify
from spotify.oauth import OAuth2
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.secret_key = "thisisasecret"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPES = "user-top-read user-read-recently-played user-library-read ugc-image-upload streaming playlist-read-private"

oauth2 = OAuth2(client_id=CLIENT_ID,
                        redirect_uri=REDIRECT_URI, 
                        scopes=SCOPES)

@app.route("/")
def login():
    auth_url = oauth2.url
    return redirect(auth_url)

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