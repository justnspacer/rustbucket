import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from api.endpoints import register_spotify_routes
from api.auth import register_auth_routes

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Add CORS support
CORS(app, origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
])

# Register routes
register_auth_routes(app)
register_spotify_routes(app)

@app.route("/")
def hello():
    return "<h1 style='color:green'>Spotify Helper API is running! 🎵</h1>"

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