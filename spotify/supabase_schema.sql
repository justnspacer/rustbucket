-- Create app_spotify table in Supabase
CREATE TABLE IF NOT EXISTS app_spotify (
    id BIGSERIAL PRIMARY KEY,
    spotify_id VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    user_id UUID REFERENCES auth.users(id),
    email VARCHAR(255),
    country VARCHAR(10),
    followers INTEGER DEFAULT 0,
    images JSONB DEFAULT '[]'::jsonb,
    product VARCHAR(50),
    external_urls JSONB DEFAULT '{}'::jsonb,
    access_token TEXT,
    refresh_token TEXT,
    app_authorized BOOLEAN DEFAULT true,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_app_spotify_spotify_id ON app_spotify(spotify_id);
CREATE INDEX IF NOT EXISTS idx_app_spotify_display_name ON app_spotify(display_name);
CREATE INDEX IF NOT EXISTS idx_app_spotify_app_authorized ON app_spotify(app_authorized);

-- Enable Row Level Security (RLS)
ALTER TABLE app_spotify ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS
-- Policy to allow read access to authorized users only
CREATE POLICY "Allow read access to authorized users" ON app_spotify
    FOR SELECT
    USING (app_authorized = true);

-- Policy to allow insert/update for authenticated users
CREATE POLICY "Allow insert for authenticated users" ON app_spotify
    FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow update for authenticated users" ON app_spotify
    FOR UPDATE
    USING (true)
    WITH CHECK (true);

-- Add comments for documentation
COMMENT ON TABLE app_spotify IS 'Stores Spotify user data for users who have authorized the app';
COMMENT ON COLUMN app_spotify.spotify_id IS 'Unique Spotify user ID';
COMMENT ON COLUMN app_spotify.display_name IS 'User display name from Spotify';
COMMENT ON COLUMN app_spotify.app_authorized IS 'Whether the user has authorized this app to access their data';
COMMENT ON COLUMN app_spotify.last_updated IS 'When the user data was last updated';
