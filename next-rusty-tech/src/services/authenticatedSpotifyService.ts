// Service to handle authenticated requests through the gatekeeper
import { useAuth } from '@/app/context/AuthContext';
export class AuthenticatedSpotifyService {
  private baseUrl: string;
  private getAuthToken: () => string | null;

  constructor(baseUrl: string = 'http://localhost:8000', getAuthToken: () => string | null) {
    this.baseUrl = baseUrl;
    this.getAuthToken = getAuthToken;
  }  private async makeRequest(endpoint: string, options: RequestInit = {}) {
    const token = this.getAuthToken();
    if (!token) {
      throw new Error('No authentication token available');
    }

    const requestOptions = {
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    // Try proxy route first (for development)
    const proxyUrl = `/api/gateway/spotify/${endpoint}`;
    try {
      const response = await fetch(proxyUrl, requestOptions);
      if (response.ok) {
        return response.json();
      }
      // If proxy fails, fall back to direct call
    } catch (error) {
      console.log('Proxy route failed, trying direct call...');
    }

    // Fallback to direct gatekeeper URL
    const directUrl = `${this.baseUrl}/api/spotify/${endpoint}`;
    const response = await fetch(directUrl, requestOptions);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(error.message || error.error || `Request failed with status ${response.status}`);
    }

    return response.json();
  }

  // Get user's Spotify profile
  async getProfile() {
    return this.makeRequest('my/profile');
  }

  // Get user's top tracks
  async getTopTracks() {
    return this.makeRequest('my/top-tracks');
  }

  // Get user's playlists
  async getPlaylists() {
    return this.makeRequest('my/playlists');
  }

  // Get currently playing track
  async getCurrentlyPlaying() {
    return this.makeRequest('my/currently-playing');
  }

  // Get public user profile (doesn't require authentication)
  async getPublicProfile(spotifyId: string) {
    return this.makeRequest(`u/${spotifyId}`);
  }

  // Search for users (doesn't require authentication)
  async searchUsers(query: string, limit: number = 20) {
    return this.makeRequest(`search-users?q=${encodeURIComponent(query)}&limit=${limit}`);
  }

  // Get list of users (doesn't require authentication)
  async getUsers(limit: number = 20) {
    return this.makeRequest(`users?limit=${limit}`);
  }

  // Get user's top artists
  async getTopArtists() {
    return this.makeRequest('my/top-artists');
  }

  // Get user's recently played tracks
  async getRecentlyPlayed() {
    return this.makeRequest('my/recently-played');
  }

  // Get user's saved tracks
  async getSavedTracks() {
    return this.makeRequest('my/saved-tracks');
  }

  // Get all dashboard data in one request
  async getDashboard() {
    return this.makeRequest('my/dashboard');
  }
}

// Hook for using the service with Next.js
export const useAuthenticatedSpotifyService = () => {
  const { getAuthToken } = useAuth();

  return new AuthenticatedSpotifyService(
    (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000').replace(':3000', ':8000'),
    getAuthToken
  );
};
