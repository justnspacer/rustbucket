# Spotify App Cleanup Summary

## Changes Made to Remove display_name and Simplify Structure

### 1. **Database Schema Alignment**

- Updated functions to match the simplified `app_spotify` table structure
- Removed all `display_name` references
- Focus on `spotify_id` and `supabase_user_id` mapping only

### 2. **Function Updates**

#### `save_or_update_user_supabase(spotify_id, supabase_user_id)`

- **Simplified**: Removed `display_name`, `access_token`, `refresh_token` parameters
- **Purpose**: Only creates/updates the mapping between Supabase user and Spotify ID
- **Fields**: `spotify_id`, `supabase_user_id`, `linked_at`, `created_at`, `updated_at`

#### `search_users_supabase(query=None, limit=20)`

- **Simplified**: Search only by `spotify_id`
- **Removed**: `display_name` search capability
- **Removed**: `app_authorized` filtering (not in new schema)

#### `save_or_update_user(spotify_id, access_token, refresh_token)`

- **Simplified**: Removed `display_name` parameter
- **Purpose**: Legacy SQLite function for local storage

#### Removed `link_supabase_user_to_spotify()`

- **Replaced**: With simplified `save_or_update_user_supabase()`
- **Reason**: Redundant functionality

### 3. **Route Updates**

#### `/spotify/save_user`

- **Updated**: Uses simplified function signatures
- **Note**: Now focuses on local SQLite storage, auth endpoints handle Supabase linking

#### `/spotify/auth/link`

- **Updated**: Uses `save_or_update_user_supabase()` directly
- **Simplified**: Clean mapping creation without extra data

#### `/spotify/test-user-data/<spotify_id>`

- **Cleaned**: Removed `display_name` from response
- **Added**: `spotify_id_confirmed` for verification

### 4. **Data Structure**

**Before (Complex):**

```python
{
    'spotify_id': 'user123',
    'display_name': 'John Doe',
    'supabase_user_id': 'uuid',
    'access_token': 'token...',
    'refresh_token': 'refresh...',
    'email': 'user@example.com',
    'followers': 150,
    # ... many other fields
}
```

**After (Simple):**

```python
{
    'spotify_id': 'user123',
    'supabase_user_id': 'uuid',
    'linked_at': '2025-01-07T...',
    'created_at': '2025-01-07T...',
    'updated_at': '2025-01-07T...'
}
```

### 5. **Benefits of Cleanup**

1. **Simpler Database Schema**: Only essential mapping data
2. **Cleaner Code**: Removed redundant parameters and functions
3. **Better Separation**: Spotify data fetched live via API, not cached
4. **Easier Maintenance**: Less data to sync and maintain
5. **Privacy Focused**: Only store necessary linking information

### 6. **Usage Notes**

- **Spotify Data**: Fetched live from Spotify API when needed
- **User Mapping**: Simple table for Supabase ↔ Spotify relationships
- **Authentication**: Handled through gatekeeper for security
- **Tokens**: Managed separately if needed for API access

The app is now streamlined to focus on the core functionality of linking Supabase users to Spotify accounts without storing redundant user profile data.
