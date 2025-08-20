"""
Spotify OAuth authentication and token management
"""
import os
import base64
from hashlib import sha256
from flask import request, redirect, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta, timezone
from functools import wraps

from .database import get_user_by_spotify_id
from .helpers import success_response, error_response
from .config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL, SCOPE
from .errors import *

load_dotenv()

# OAuth client (initialized on first use)
_oauth_client = None

def get_oauth_client():
    """Get or initialize Spotify OAuth client"""
    global _oauth_client
    if _oauth_client is None:
        _oauth_client = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI, 
            scope=SCOPE
        )
    return _oauth_client

def require_spotify_auth(f):
    """Decorator to require Spotify authentication for endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from .database import get_supabase_client
        
        # Get authenticated user from Supabase context (passed by Next.js middleware)
        user_data = get_authenticated_user(request)
        if not user_data:
            return error_response(
                message="User authentication required", 
                status_code=401, 
                error_code=AUTH_REQUIRED
            )
        
        user_id = user_data['id']
        
        # Check if user has linked Spotify account
        supabase = get_supabase_client()
        spotify_result = supabase.table('app_spotify').select('*').eq('user_id', user_id).execute()
        if not spotify_result.data:
            return error_response(
                message="Spotify authorization required", 
                status_code=403, 
                error_code=SPOTIFY_UNAUTHORIZED
            )
        
        spotify_user = spotify_result.data[0]
        
        # Check if Spotify tokens are still valid
        now = datetime.now(timezone.utc)
        expires_at = datetime.fromisoformat(spotify_user['expires_at'].replace('Z', '+00:00'))
        
        if now >= expires_at:
            # Try to refresh the token
            refresh_token = base64.urlsafe_b64decode(spotify_user['encrypted_refresh_token'] + '==').decode('utf-8')
            try:
                new_token_info = refresh_spotify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
                if new_token_info and 'access_token' in new_token_info:
                    # Update tokens in database
                    expires_in = new_token_info.get('expires_in', 3600)
                    supabase.table('app_spotify').update({
                        'encrypted_access_token': base64_url_encode(new_token_info['access_token'].encode('utf-8')),
                        'expires_at': (datetime.now(timezone.utc) + timedelta(seconds=expires_in)).isoformat()
                    }).eq('user_id', user_id).execute()
                    
                    # Update the spotify_user data with new token
                    spotify_user['encrypted_access_token'] = base64_url_encode(new_token_info['access_token'].encode('utf-8'))
                else:
                    return error_response(
                        message="Spotify token refresh failed", 
                        status_code=403, 
                        error_code=TOKEN_EXPIRED
                    )
            except Exception as e:
                print(f"Token refresh failed: {e}")
                return error_response(
                    message="Spotify token refresh failed", 
                    status_code=403, 
                    error_code=TOKEN_EXPIRED
                )
        
        # Decode the access token for use
        access_token = base64.urlsafe_b64decode(spotify_user['encrypted_access_token'] + '==').decode('utf-8')
        
        # Attach user and token info to request context
        request.supabase_user = user_data
        request.spotify_user = spotify_user
        request.spotify_token = access_token
        return f(*args, **kwargs)
    return decorated_function

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

def generate_random_string(length=16):
    """Generate a random string for OAuth state"""
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def base64_url_encode(data):
    """Encode data for URL-safe base64"""
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def refresh_spotify_token(refresh_token, client_id, client_secret):
    """Refresh Spotify access token"""
    url = TOKEN_URL
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': f'Basic {base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Failed to refresh token')

def exchange_code_for_tokens(code, code_verifier):
    """Exchange authorization code for access and refresh tokens"""
    url = TOKEN_URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
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

def register_auth_routes(app):
    """Register OAuth routes with Flask app"""
    
    @app.route("/api/spotify/authorize")
    def spotify_authorize():
        user_id = request.headers.get('x-user-id')
        user_id = 'aa9710dd-680d-4c47-bb12-8f70aa069c43'  # TODO: Remove hardcode
        if not user_id:
            return error_response(
                message="User authentication required", 
                status_code=401, 
                error_code=AUTH_REQUIRED
            )
        
        # Generate OAuth parameters
        state_random = generate_random_string(16)
        code_verifier = generate_random_string(128)
        code_challenge = base64_url_encode(sha256(code_verifier.encode('utf-8')).digest())
        
        # Encode user_id into the state parameter
        state_data = {
            'user_id': user_id,
            'random': state_random
        }
        encoded_state = base64_url_encode(json.dumps(state_data).encode('utf-8'))
        
        # Store OAuth data in Supabase temporarily
        from .database import get_supabase_client
        try:
            supabase = get_supabase_client()
            supabase.table('temp_oauth_state').upsert({
                'state_key': encoded_state,
                'user_id': user_id,
                'code_verifier': code_verifier,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'expires_at': (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
            }).execute()
        except Exception as e:
            print(f"Error storing OAuth state: {e}")
            return error_response(
                message="Failed to initiate OAuth flow", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

        auth_url = (
            f"https://accounts.spotify.com/authorize?"
            f"client_id={CLIENT_ID}&"
            f"response_type=code&"
            f"redirect_uri={REDIRECT_URI}&"
            f"code_challenge_method=S256&"
            f"code_challenge={code_challenge}&"
            f"state={encoded_state}&"
            f"scope={SCOPE}"
        )
        return redirect(auth_url)
    
    @app.route("/api/spotify/callback")
    def spotify_callback():
        from .database import get_supabase_client
        
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")

        if error:
            return error_response(
                message=f"Spotify authorization failed: {error}", 
                status_code=400, 
                error_code=SPOTIFY_UNAUTHORIZED
            )

        if not code or not state:
            return error_response(
                message="Missing required parameters", 
                status_code=400, 
                error_code=VALIDATION_ERROR
            )

        # Decode the state to get user_id
        try:
            state_data = json.loads(base64.urlsafe_b64decode(state + '==').decode('utf-8'))
            user_id = state_data.get('user_id')
        except Exception as e:
            print(f"Error decoding state: {e}")
            return error_response(
                message="Invalid state parameter", 
                status_code=400, 
                error_code=VALIDATION_ERROR
            )

        if not user_id:
            return error_response(
                message="Invalid state parameter", 
                status_code=400, 
                error_code=VALIDATION_ERROR
            )

        # Retrieve OAuth data from Supabase
        try:
            supabase = get_supabase_client()
            oauth_result = supabase.table('temp_oauth_state').select('*').eq('state_key', state).execute()
            if not oauth_result.data:
                return error_response(
                    message="Invalid or expired state", 
                    status_code=400, 
                    error_code=VALIDATION_ERROR
                )
            
            oauth_data = oauth_result.data[0]
            code_verifier = oauth_data['code_verifier']
            
        except Exception as e:
            print(f"Error retrieving OAuth data: {e}")
            return error_response(
                message="OAuth state retrieval failed", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

        # Exchange code for tokens
        token_info = exchange_code_for_tokens(code, code_verifier)
        if not token_info:
            return error_response(
                message="Failed to obtain tokens", 
                status_code=400, 
                error_code=SPOTIFY_API_ERROR
            )

        # Get Spotify user info
        try:            
            sp = spotipy.Spotify(auth=token_info['access_token'])
            spotify_user_info = sp.current_user()
            spotify_id = spotify_user_info['id']
        except Exception as e:
            print(f"Error getting Spotify user info: {e}")
            return error_response(
                message="Failed to get Spotify user info", 
                status_code=500, 
                error_code=SPOTIFY_API_ERROR
            )

        # Store or update user's Spotify account linkage
        try:
            existing_link = supabase.table('app_spotify').select('*').eq('user_id', user_id).execute()
            
            if existing_link.data:
                # Update existing record
                supabase.table('app_spotify').update({
                    'spotify_id': spotify_id,
                    'encrypted_access_token': base64_url_encode(token_info['access_token'].encode('utf-8')),
                    'encrypted_refresh_token': base64_url_encode(token_info['refresh_token'].encode('utf-8')),
                    'expires_at': (datetime.now(timezone.utc) + timedelta(seconds=token_info['expires_in'])).isoformat(),
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).eq('user_id', user_id).execute()
                
                message = "Spotify account re-linked successfully"
            else:
                # Create new record
                supabase.table('app_spotify').insert({
                    'user_id': user_id,
                    'spotify_id': spotify_id,
                    'encrypted_access_token': base64_url_encode(token_info['access_token'].encode('utf-8')),
                    'encrypted_refresh_token': base64_url_encode(token_info['refresh_token'].encode('utf-8')),
                    'expires_at': (datetime.now(timezone.utc) + timedelta(seconds=token_info['expires_in'])).isoformat(),
                    'linked_at': datetime.now(timezone.utc).isoformat(),
                    'created_at': datetime.now(timezone.utc).isoformat(),
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }).execute()
                
                message = "Spotify account linked successfully"
                
        except Exception as e:
            print(f"Error storing tokens: {e}")
            return error_response(
                message="Failed to store tokens", 
                status_code=500, 
                error_code=INTERNAL_ERROR
            )

        # Clean up temporary OAuth data
        try:
            cleanup_result = supabase.table('temp_oauth_state').delete().eq('state_key', state).execute()
            print(f"OAuth state cleanup: {len(cleanup_result.data) if cleanup_result.data else 0} records deleted")
        except Exception as cleanup_error:
            print(f"Warning: Failed to cleanup OAuth state: {cleanup_error}")

        return success_response(
            data={'spotify_id': spotify_id}, 
            message=message
        )
