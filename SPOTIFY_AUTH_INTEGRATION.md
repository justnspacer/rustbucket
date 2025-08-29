# Supabase Auth Session Integration with Spotify via Gatekeeper

This guide explains how to pass Supabase authentication sessions from your Next.js app to your Spotify app through the gatekeeper.

## Architecture Overview

```
Next.js App → Gatekeeper (validates Supabase JWT) → Spotify App (receives user info)
```

## Setup Steps

### 1. Database Setup

First, create the user mapping table in your Supabase database:

```sql
-- Run the SQL in create_user_mapping_table.sql
```

### 2. Environment Variables

Make sure these environment variables are set in your projects:

**Gatekeeper (.env):**

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

**Spotify App (.env):**

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

**Next.js App (.env.local):**

```env
NEXT_PUBLIC_GATEKEEPER_URL=http://localhost:8000
```

### 3. Start the Services

1. **Start Gatekeeper:**

```bash
cd gatekeeper
uvicorn main:app --reload --port 8000
```

2. **Start Spotify App:**

```bash
cd spotify
python run.py
```

3. **Start Next.js App:**

```bash
cd next-rusty-tech
npm run dev
```

## Usage Flow

### 1. Authentication Flow

1. User logs in through your Next.js app using Supabase auth
2. JWT token is stored in cookies
3. When making requests to Spotify features, the token is sent to gatekeeper
4. Gatekeeper validates the token and extracts user info
5. User info is passed to the Spotify app via headers

### 2. Spotify Account Linking

Before users can access their Spotify data, they need to:

1. **Authorize with Spotify first:** Visit `http://localhost:5000/spotify/login` to complete Spotify OAuth
2. **Link their account:** Use the `linkSpotifyAccount(spotifyId)` method with their Spotify ID

### 3. API Endpoints

#### Authenticated Endpoints (require Supabase auth)

- `GET /api/spotify/auth/profile` - Get user's linked Spotify profile
- `GET /api/spotify/auth/top-tracks` - Get user's top tracks
- `GET /api/spotify/auth/playlists` - Get user's playlists
- `GET /api/spotify/auth/currently-playing` - Get currently playing track

#### Public Endpoints (no auth required)

- `GET /api/spotify/users` - List all users
- `GET /api/spotify/search-users?q=query` - Search users
- `GET /api/spotify/u/{spotify_id}` - Get public profile

### 4. Frontend Usage

```tsx
import { useAuthenticatedSpotifyService } from '@/services/authenticatedSpotifyService';

function MyComponent() {
  const spotifyService = useAuthenticatedSpotifyService();

  const handleGetProfile = async () => {
    try {
      const profile = await spotifyService.getProfile();
      console.log(profile);
    } catch (error) {
      if (error.message.includes('not linked')) {
        // Show Spotify linking UI
        await spotifyService.linkSpotifyAccount('user_spotify_id');
      }
    }
  };
}
```

## Security Features

1. **JWT Validation:** Gatekeeper validates Supabase JWT tokens
2. **User Isolation:** Each user can only access their own data
3. **Token Refresh:** Spotify tokens are automatically refreshed when expired
4. **RLS Policies:** Database-level security with Row Level Security

## Error Handling

Common errors and solutions:

1. **"Authentication required"** - User not logged in to Supabase
2. **"Spotify account not linked"** - User needs to link their Spotify account
3. **"Unable to access Spotify data"** - Spotify tokens may be expired or invalid

## Example Component

See `SpotifyDashboard.tsx` for a complete example of how to use the authenticated Spotify service in a React component.

## Testing

1. **Test authentication:** Visit `/user` endpoint on gatekeeper
3. **Test data access:** Use any of the authenticated endpoints

## Troubleshooting

### CORS Issues

If you encounter CORS errors like:

```
Access to fetch at 'http://localhost:8000/api/spotify/auth/profile' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution 1: CORS Middleware (Recommended)**
The gatekeeper has been updated with CORS middleware. If you're still seeing errors:

1. Restart the gatekeeper service
2. Verify your Next.js app is running on `http://localhost:3000`
3. Check the CORS origins in `gatekeeper/main.py`

**Solution 2: Alternative Origins**
If your Next.js app runs on a different port, update the CORS origins in `gatekeeper/main.py`:

```python
allow_origins=[
    "http://localhost:3000",  # Default Next.js
    "http://localhost:3001",  # Alternative port
    "http://your-domain.com", # Production domain
],
```

**Solution 3: Development Proxy**
Alternatively, use Next.js rewrites in `next.config.js`:

```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/gateway/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};
```

### Other Common Issues

1. **Check logs:** Both gatekeeper and Spotify app log errors
2. **Verify tokens:** Ensure Supabase JWT tokens are valid
3. **Check database:** Verify user mapping table exists and has correct data
4. **Network issues:** Ensure all services are running on correct ports
