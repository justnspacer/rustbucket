-- Create table to map Supabase users to Spotify accounts
CREATE TABLE IF NOT EXISTS app_spotify (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    spotify_id VARCHAR(255) NOT NULL,
    linked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    encrypted_access_token TEXT NOT NULL,
    encrypted_refresh_token TEXT NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Ensure one-to-one mapping
    UNIQUE(user_id),
    UNIQUE(spotify_id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_app_spotify_user_id 
ON app_spotify(supabase_user_id);

CREATE INDEX IF NOT EXISTS idx_app_spotify_spotify_id 
ON app_spotify(spotify_id);

-- Index for faster user token lookups
CREATE INDEX idx_app_spotify_user_id ON app_spotify(user_id);
CREATE INDEX idx_app_spotify_expires_at ON app_spotify(expires_at);

-- Add RLS (Row Level Security) policies if needed
ALTER TABLE app_spotify ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to see their own mappings
CREATE POLICY "Users can view their own spotify mapping" 
ON app_spotify FOR SELECT 
USING (auth.uid() = user_id);

-- Policy to allow users to insert their own mappings
CREATE POLICY "Users can insert their own spotify mapping" 
ON app_spotify FOR INSERT 
WITH CHECK (auth.uid() = user_id);

-- Policy to allow users to update their own mappings
CREATE POLICY "Users can update their own spotify mapping" 
ON app_spotify FOR UPDATE 
USING (auth.uid() = user_id);
