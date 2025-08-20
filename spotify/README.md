# Spotify Helper API

A Flask-based REST API for Spotify integration with Supabase authentication and Next.js frontend support.

## Project Structure

```
├── api/                    # Organized API modules
│   ├── __init__.py        # Package initialization
│   ├── auth.py            # OAuth flow and authentication decorators
│   ├── config.py          # Configuration and environment variables
│   ├── database.py        # Supabase client and database utilities
│   ├── endpoints.py       # Spotify API endpoints
│   ├── errors.py          # Error codes and constants
│   ├── helpers.py         # Response formatting utilities
│   └── spotify_client.py  # Spotify API client utilities
├── static/                # Static assets (CSS, JS)
├── templates/             # HTML templates
├── migrations/            # Database migration files
├── _backup/               # Backup of original files
├── cli.py                 # Database utilities and testing
├── run.py                 # Main Flask application
├── requirements.txt       # Python dependencies
└── create_app_spotify.sql # Database schema
```

## Features

### Authentication Flow
- **OAuth 2.0 PKCE**: Secure Spotify authentication
- **Next.js Integration**: Header-based user authentication
- **Token Management**: Automatic refresh with encrypted storage
- **Supabase Storage**: Secure OAuth state and token management

### API Endpoints

#### Public Profile Endpoints
- `GET /api/spotify/profile/{spotify_id}` - Get user profile
- `GET /api/spotify/profile/{spotify_id}/playlists` - Get user playlists
- `GET /api/spotify/profile/{spotify_id}/top-tracks` - Get user's top tracks
- `GET /api/spotify/profile/{spotify_id}/top-artists` - Get user's top artists

#### Authenticated User Endpoints
- `GET /api/spotify/my/profile` - Get current user profile
- `GET /api/spotify/my/playlists` - Get current user playlists
- `GET /api/spotify/my/saved-tracks` - Get saved tracks
- `GET /api/spotify/my/top-tracks` - Get top tracks
- `GET /api/spotify/my/top-artists` - Get top artists
- `GET /api/spotify/my/recently-played` - Get recently played
- `GET /api/spotify/my/following` - Get followed artists/users

#### Playlist Endpoints
- `GET /api/spotify/playlists/{playlist_id}` - Get playlist details
- `GET /api/spotify/playlists/{playlist_id}/tracks` - Get playlist tracks

#### Search Endpoints
- `GET /api/spotify/search/users?q={query}` - Search for users with linked Spotify accounts
- `GET /api/spotify/search?q={query}&type={types}` - Search Spotify catalog (authenticated)
- `GET /api/spotify/search/tracks?q={query}` - Search for tracks specifically
- `GET /api/spotify/search/artists?q={query}` - Search for artists specifically
- `GET /api/spotify/search/albums?q={query}` - Search for albums specifically
- `GET /api/spotify/search/playlists?q={query}` - Search for playlists specifically

#### Discovery Endpoints
- `GET /api/spotify/recommendations` - Get music recommendations based on seeds
- `GET /api/spotify/genres` - Get available genre seeds for recommendations

#### Authentication Endpoints
- `GET /api/spotify/authorize` - Initiate OAuth flow
- `GET /api/spotify/callback` - OAuth callback handler

## Search Functionality

### User Search
Find other users who have linked their Spotify accounts:

```bash
GET /api/spotify/search/users?q=spotify_username&limit=20&offset=0
```

**Parameters:**
- `q` (optional) - Search query for Spotify username
- `limit` (optional) - Number of results (max 50, default 20)
- `offset` (optional) - Pagination offset (default 0)

**Response includes:**
- User's Spotify ID and display name
- Profile images and follower count
- Account linking date
- Spotify profile URL

### Music Content Search
Search the Spotify catalog for music content:

```bash
# General search (supports multiple types)
GET /api/spotify/search?q=artist:Beatles track:Yesterday&type=track,artist&limit=10

# Specific content type searches
GET /api/spotify/search/tracks?q=Yesterday Beatles
GET /api/spotify/search/artists?q=Beatles
GET /api/spotify/search/albums?q=Abbey Road
GET /api/spotify/search/playlists?q=Rock Classics
```

**Search Parameters:**
- `q` (required) - Search query (supports Spotify search syntax)
- `type` (optional) - Content types: `track,artist,album,playlist` (default: all)
- `limit` (optional) - Number of results per type (max 50, default 20)
- `offset` (optional) - Pagination offset (default 0)
- `market` (optional) - ISO country code (default: US)

**Spotify Search Syntax Examples:**
- `artist:Beatles` - Search for Beatles as artist
- `album:Abbey Road` - Search for Abbey Road album
- `track:Yesterday` - Search for Yesterday track
- `year:1969` - Search for music from 1969
- `genre:rock` - Search for rock music

### Music Recommendations
Get personalized music recommendations:

```bash
GET /api/spotify/recommendations?seed_artists=4NHQUGzhtTLFvgF5SZesLK&seed_tracks=0c6xIDDpzE81m2q797ordA&limit=10
```

**Seed Parameters (at least one required):**
- `seed_tracks[]` - Array of track IDs (max 5)
- `seed_artists[]` - Array of artist IDs (max 5)  
- `seed_genres[]` - Array of genre names (max 5)

**Audio Feature Tuning (optional):**
- `target_*` - Target value for audio features (0.0-1.0)
- `min_*` - Minimum value for audio features
- `max_*` - Maximum value for audio features

**Available Audio Features:**
- `acousticness`, `danceability`, `energy`, `instrumentalness`
- `liveness`, `loudness`, `speechiness`, `tempo`, `valence`

**Example with audio features:**
```bash
GET /api/spotify/recommendations?seed_genres=rock&target_energy=0.8&min_danceability=0.5
```

### Available Genres
Get list of available genre seeds:

```bash
GET /api/spotify/genres
```

## Setup

### Environment Variables
```bash
# Spotify API
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:5001/api/spotify/callback

# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Flask
FLASK_DEBUG=true
```

### Database Schema
Run the SQL schema in `create_app_spotify.sql` to set up required tables:
- `app_spotify` - User-Spotify account linkages
- `temp_oauth_state` - Temporary OAuth state storage

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py

# Or use CLI utilities
python cli.py --help
```

## Architecture

### Code Organization
- **Separation of Concerns**: Clear distinction between auth, endpoints, database, and utilities
- **Modular Design**: Each module has a specific responsibility
- **Error Handling**: Standardized error responses with specific error codes
- **Type Safety**: Proper typing and validation

### Security Features
- **Token Encryption**: Access/refresh tokens stored with base64 encoding
- **OAuth State Management**: Secure state parameter handling with expiration
- **Request Validation**: Proper parameter validation and sanitization
- **CORS Configuration**: Configured for specific frontend origins

### Database Design
- **RLS Policies**: Row-level security for user data isolation
- **Automatic Cleanup**: Expired OAuth states automatically cleaned up
- **Efficient Indexing**: Optimized queries for user and Spotify ID lookups

## API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Success message",
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error message",
  "error_code": "ERROR_CODE",
  "details": { ... }
}
```

### Error Codes
- `AUTH_REQUIRED` - User authentication required
- `SPOTIFY_UNAUTHORIZED` - Spotify authorization required
- `TOKEN_EXPIRED` - Spotify token expired
- `VALIDATION_ERROR` - Request validation failed
- `SPOTIFY_API_ERROR` - Spotify API error
- `NOT_FOUND` - Resource not found
- `RATE_LIMITED` - API rate limit exceeded
- `INTERNAL_ERROR` - Server error

## Development

### CLI Utilities
```bash
# Test database connection
python cli.py test-db

# Clean up expired OAuth states
python cli.py cleanup-oauth

# Show user linkage info
python cli.py show-user <user_id>

# List all linked users
python cli.py list-users
```

### Next.js Integration
The API expects these headers for authenticated requests:
- `x-user-id` - Supabase user ID
- `x-user-email` - User email
- `x-user-metadata` - User metadata (JSON string)

### Token Flow
1. User clicks "Connect Spotify" in Next.js app
2. Frontend redirects to `/api/spotify/authorize`
3. User completes OAuth flow on Spotify
4. Callback stores encrypted tokens in Supabase
5. Subsequent API calls use stored tokens automatically
6. Tokens refresh automatically when expired

## Contributing

When adding new endpoints:
1. Add the endpoint function in `api/endpoints.py`
2. Register it in the `register_spotify_routes()` function
3. Add appropriate error handling and response formatting
4. Update this README with the new endpoint documentation

When modifying authentication:
1. Update `api/auth.py` for auth logic changes
2. Update `api/database.py` for database schema changes
3. Run migration scripts if needed
4. Test with CLI utilities
