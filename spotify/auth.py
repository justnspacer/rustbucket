import os
import base64
from hashlib import sha256
from flask import request, redirect, session, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests
from supabase_client import supabase
import json
from datetime import datetime, timedelta
from helpers import success_response, error_response, paginated_response
import random
import string
from functools import wraps
import token_manager

load_dotenv()

# Authentication errors
AUTH_REQUIRED = "AUTH_REQUIRED"
INVALID_TOKEN = "INVALID_TOKEN"
TOKEN_EXPIRED = "TOKEN_EXPIRED"

# Spotify API errors
SPOTIFY_UNAUTHORIZED = "SPOTIFY_UNAUTHORIZED"

# General errors
VALIDATION_ERROR = "VALIDATION_ERROR"
NOT_FOUND = "NOT_FOUND"
INTERNAL_ERROR = "INTERNAL_ERROR"

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = os.getenv("TOKEN_URL")
SCOPE = os.getenv("SCOPE")


oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI, 
                        scope=SCOPE)

def require_spotify_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Read Bearer token from Authorization header
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return error_response(message="Missing or invalid Authorization header", status_code=401, error_code=AUTH_REQUIRED)
        bearer_token = auth_header.split(' ', 1)[1]

        # Find user by encrypted_access_token in DB
        user_result = supabase.table('app_spotify').select('*').eq('encrypted_access_token', bearer_token).execute()
        if not user_result.data:
            return error_response(message="Spotify authorization required", status_code=403, error_code=SPOTIFY_UNAUTHORIZED)
        user = user_result.data[0]

        # Attach token and user to request context
        request.spotify_token = bearer_token
        request.spotify_user = user
        return f(*args, **kwargs)
    return decorated_function

def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def base64_url_encode(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def store_tokens_in_supabase(user_id, token_info):
    """Store the access and refresh tokens in Supabase"""
    try:
        result = supabase.table('app_spotify').update({
            'encrypted_access_token': base64_url_encode(token_info['access_token']),
            'encrypted_refresh_token': base64_url_encode(token_info['refresh_token']),
            'expires_at': datetime.now(datetime.timezone.utc) + timedelta(seconds=token_info['expires_in'])
        }).eq('user_id', user_id).execute()
        return result
    except Exception as e:
        print(f"Error storing tokens in Supabase: {e}")
        return None

def exchange_code_for_tokens(code, code_verifier):
    url = TOKEN_URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error exchanging code for tokens: {response.text}")
        return None

def get_temp_oauth_data(user_id):
    """Retrieve temporary OAuth data from Flask session"""
    try:
        data = session.get(f'oauth_data_{user_id}')
        if data:
            print(f"Temporary OAuth data for user {user_id} retrieved successfully.")
            return data
    except Exception as e:
        print(f"Error retrieving temporary OAuth data: {e}")
    return None

def store_temp_oauth_data(user_id, data):
    """Store temporary OAuth data in Flask session"""
    try:
        session[f'oauth_data_{user_id}'] = data
        return True
    except Exception as e:
        print(f"Error storing temporary OAuth data: {e}")
        return None

class TokenNotFoundError(Exception):
    """Custom exception for when a token is not found."""
    pass

def get_authenticated_user(request):
    """Extract authenticated user info from request headers"""
    user_id = request.headers.get('x-user-id')
    user_email = request.headers.get('x-user-email')
    user_metadata = request.headers.get('x-user-metadata')
    
    if user_id:
        user_data = {
            'id': user_id,
            'email': user_email,
            'metadata': {}
        }
        
        # Parse metadata if present
        if user_metadata:
            try:
                user_data['metadata'] = json.loads(user_metadata.replace("'", '"'))
            except:
                pass
        
        return user_data
    return None

def refresh_spotify_token(refresh_token, client_id, client_secret):
    url = TOKEN_URL
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': f'Basic {client_id}:{client_secret}'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to refresh token')

def get_spotify_for_current_user():
    token_info = oauth.get_access_token()
    sp = spotipy.Spotify(auth=token_info["access_token"])    
    # Check if the token has expired
    now = datetime.now()
    expires_at = datetime.fromtimestamp(token_info['expires_at'])
    if now >= expires_at:
        # Refresh the token
        refresh_token = token_info['refresh_token']
        new_access_token = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
        token_info['access_token'] = new_access_token
        token_info['expires_at'] = (now + datetime.timedelta(seconds=3600)).timestamp() #1 hour variable, move to env
    return sp, token_info["access_token"], token_info["refresh_token"] 


def get_user(spotify_id):
    """Get a specific user by spotify_id"""
    try:
        result = supabase.table('app_spotify').select('*').eq('spotify_id', spotify_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_spotify_by_user_id(user_id):
    """Get Spotify client and user info for a specific user ID from Supabase"""
    try:
        # Get user data from Supabase
        user_data = get_user(user_id)
        if not user_data:
            return None, None, None
        
        access_token = user_data.get('access_token')
        refresh_token = user_data.get('refresh_token')
        
        if not access_token:
            return None, None, None
        
        # Create Spotify client with the user's access token
        sp = spotipy.Spotify(auth=access_token)
        
        # Check if token is still valid by trying to get user info
        try:
            user_info = sp.current_user()
            return sp, access_token, refresh_token
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:  # Unauthorized - token expired
                # Try to refresh the token
                if refresh_token:
                    try:
                        new_access_token = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
                        
                        # Update token in Supabase
                        supabase.table('app_spotify').update({
                            'access_token': new_access_token,
                            'last_updated': datetime.now(datetime.timezone.utc).isoformat()
                        }).eq('spotify_id', user_id).execute()
                        
                        # Create new Spotify client with refreshed token
                        sp = spotipy.Spotify(auth=new_access_token)
                        return sp, new_access_token, refresh_token
                    except Exception as refresh_error:
                        print(f"Failed to refresh token for user {user_id}: {refresh_error}")
                        return None, None, None
            return None, None, None
    except Exception as e:
        print(f"Error getting Spotify client for user {user_id}: {e}")
        return None, None, None

def spotify_auth(app):

    @app.route("/api/spotify/authorize")
    def spotify_authorize():
        state = generate_random_string(16)
        code_verifier = generate_random_string(128)
        code_challenge = base64_url_encode(sha256(code_verifier.encode('utf-8')).digest())

        user_id = request.headers.get('x-user-id')
        if user_id:
            store_temp_oauth_data(user_id, {
                'state': state,
                'code_verifier': code_verifier
            })

        auth_url = (
            f"https://accounts.spotify.com/authorize?"
            f"client_id={CLIENT_ID}&"
            f"response_type=code&"
            f"redirect_uri={REDIRECT_URI}&"
            f"code_challenge_method=S256&"
            f"code_challenge={code_challenge}&"
            f"state={state}&"
            f"scope={SCOPE}"
        )
        return redirect(auth_url)
    
    @app.route("/api/spotify/callback")
    def spotify_callback():
        code = request.args.get("code")
        state = request.args.get("state")
        user_id = request.headers.get("x-user-id")

        if not code or not state or not user_id:
            return {"error": "Missing required parameters"}, 400

        # Retrieve the stored code_verifier using the user_id
        temp_oauth_data = get_temp_oauth_data(user_id)
        if not temp_oauth_data or temp_oauth_data["state"] != state:
            return {"error": "Invalid state"}, 400

        code_verifier = temp_oauth_data["code_verifier"]

        # Exchange the authorization code for access and refresh tokens
        token_info = exchange_code_for_tokens(code, code_verifier)
        if not token_info:
            return {"error": "Failed to obtain tokens"}, 400

        # Store the tokens in Supabase
        store_tokens_in_supabase(user_id, token_info)

        # Clean up temporary OAuth data
        session.pop(f'oauth_data_{user_id}', None)

        return {"message": "Authorization successful"}, 200