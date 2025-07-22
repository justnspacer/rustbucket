// Spotify API Types
export interface SpotifyImage {
  url: string;
  height?: number;
  width?: number;
}

export interface SpotifyFollowers {
  total: number;
  href?: string;
}

export interface SpotifyExternalUrls {
  spotify: string;
}

export interface SpotifyUser {
  id: string;
  spotify_id: string;
  display_name: string;
  images?: SpotifyImage[];
  followers: SpotifyFollowers | number;
  country?: string;
  product?: string;
  last_updated?: string;
  external_urls?: SpotifyExternalUrls;
  email?: string;
  explicit_content?: {
    filter_enabled: boolean;
    filter_locked: boolean;
  };
  href?: string;
  type?: string;
  uri?: string;
}

export interface SpotifyArtist {
  id: string;
  name: string;
  images?: SpotifyImage[];
  popularity?: number;
  external_urls?: SpotifyExternalUrls;
  followers?: SpotifyFollowers;
  genres?: string[];
  href?: string;
  type?: string;
  uri?: string;
}

export interface SpotifyAlbum {
  id: string;
  name: string;
  images?: SpotifyImage[];
  release_date?: string;
  total_tracks?: number;
  external_urls?: SpotifyExternalUrls;
  artists?: SpotifyArtist[];
  album_type?: string;
  href?: string;
  type?: string;
  uri?: string;
}

export interface SpotifyTrack {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  album: SpotifyAlbum;
  popularity?: number;
  duration_ms?: number;
  explicit?: boolean;
  external_urls?: SpotifyExternalUrls;
  href?: string;
  is_local?: boolean;
  preview_url?: string;
  track_number?: number;
  type?: string;
  uri?: string;
  added_at?: string;
}

export interface SpotifyPlaylist {
  id: string;
  name: string;
  description?: string;
  images?: SpotifyImage[];
  tracks: {
    total: number;
    items?: Array<{
      track: SpotifyTrack;
      added_at: string;
    }>;
  };
  public?: boolean;
  external_urls?: SpotifyExternalUrls;
  followers?: SpotifyFollowers;
  href?: string;
  owner?: SpotifyUser;
  snapshot_id?: string;
  type?: string;
  uri?: string;
}

export interface SpotifyCurrentlyPlaying {
  item?: SpotifyTrack;
  is_playing: boolean;
  progress_ms?: number;
  timestamp?: number;
  context?: {
    type: string;
    href: string;
    external_urls: SpotifyExternalUrls;
    uri: string;
  };
  repeat_state?: string;
  shuffle_state?: boolean;
  device?: {
    id: string;
    is_active: boolean;
    is_private_session: boolean;
    is_restricted: boolean;
    name: string;
    type: string;
    volume_percent: number;
  };
}

// API Response Types
export interface SpotifySearchResponse {
  users: SpotifyUser[];
  total?: number;
  limit?: number;
  offset?: number;
}

export interface SpotifyTopItemsResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
  href: string;
  next?: string;
  previous?: string;
}

export interface SpotifyUserProfileResponse {
  user: SpotifyUser;
  is_public?: boolean;
}

// Component Props Types
export interface SpotifySearchProps {
  onUserSelect?: (userId: string) => void;
  className?: string;
}

export interface SpotifyUserProfileProps {
  userId: string;
  isPublic?: boolean;
  className?: string;
}

export interface SpotifyLayoutProps {
  children: React.ReactNode;
  className?: string;
}

// Error Types
export interface SpotifyApiError {
  error: {
    status: number;
    message: string;
  };
}

// Database Types (for your backend)
export interface DbSpotifyUser {
  id: number;
  spotify_id: string;
  display_name?: string;
  email?: string;
  country?: string;
  product?: string;
  followers?: number;
  images?: string; // JSON string
  last_updated: Date;
  created_at: Date;
  access_token?: string;
  refresh_token?: string;
  token_expires_at?: Date;
}
