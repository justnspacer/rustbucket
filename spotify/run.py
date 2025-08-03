import os
from flask import Flask
from dotenv import load_dotenv
from supabase_client import supabase
from datetime import datetime
from flask_cors import CORS
from app import register_spotify_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "thisisasecret"

# Add CORS support
CORS(app, origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
])

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = os.getenv("TOKEN_URL")
SCOPE = "user-top-read user-read-recently-played user-read-currently-playing user-library-read ugc-image-upload streaming playlist-read-private streaming user-read-private user-read-email user-modify-playback-state user-read-playback-state"
DEVICE_ID = "your_device_id"

# Register Spotify routes
register_spotify_routes(app, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL, SCOPE, DEVICE_ID)

if __name__ == '__main__':
     # Enable debug mode for hot reloading
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=debug_mode,
        use_reloader=True,  # Enable auto-reload on file changes
        use_debugger=True   # Enable debugger
    )