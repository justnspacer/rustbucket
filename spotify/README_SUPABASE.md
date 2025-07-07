# Spotify User Search Integration with Supabase

This Flask application integrates with Spotify API and Supabase to allow users to authorize the app and search for other users who have also authorized it.

## Features

- Spotify OAuth integration
- Store user data in both local SQLite and Supabase
- Search for users who have authorized the app
- Public user profiles
- RESTful API endpoints

## Setup Instructions

### 1. Install Dependencies

```bash
cd spotify
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the spotify directory with the following variables:

```env
# Spotify API Keys
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret

# Supabase Configuration
SUPABASE_URL=https://divoxddsmcxnlbdooxzt.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Supabase Setup

Run the SQL script in `supabase_schema.sql` in your Supabase SQL editor to create the `app_spotify` table:

```sql
-- Copy and paste the contents of supabase_schema.sql into Supabase SQL editor
```

### 4. Run the Application

```bash
python run.py
```

## API Endpoints

### User Management

- `GET /spotify/login` - Initiate Spotify OAuth
- `GET /spotify/callback` - OAuth callback
- `GET /spotify/save_user` - Save current user to databases

### User Search

- `GET /spotify/search` - Search users page
- `GET /spotify/search-users?q=query` - Search users API
- `GET /spotify/users` - List all authorized users
- `GET /spotify/u/<spotify_id>` - View public user profile

### Spotify Data

- `GET /spotify/top-artists-and-tracks` - Get user's top content
- `GET /spotify/currently-playing` - Get currently playing track
- `GET /spotify/playlists` - Get user's playlists
- `GET /spotify/saved-tracks` - Get user's saved tracks

## Database Schema

The `app_spotify` table in Supabase stores:

- `spotify_id` - Unique Spotify user ID
- `display_name` - User's display name
- `email` - User's email (if available)
- `country` - User's country
- `followers` - Number of followers
- `images` - Profile images (JSON)
- `product` - Spotify subscription type
- `access_token` - Spotify access token
- `refresh_token` - Spotify refresh token
- `app_authorized` - Whether user authorized the app
- `last_updated` - When data was last updated

## Usage Flow

1. User visits `/spotify/login` to authorize the app
2. After authorization, user visits `/spotify/save_user` to save their data
3. Users can search for other authorized users at `/spotify/search`
4. Public profiles are available at `/spotify/u/<spotify_id>`

## Security Notes

- Access tokens are stored securely in Supabase
- Row Level Security (RLS) is enabled on the app_spotify table
- Only authorized users are visible in search results
- Public profiles don't expose sensitive token data
