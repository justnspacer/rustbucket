"use client";
import { useState, useEffect } from "react";
import { useAuth } from "@/app/context/AuthContext";
import { useAuthenticatedSpotifyService } from "@/services/authenticatedSpotifyService";

interface SpotifyProfile {
  supabase_user: {
    id: string;
    email: string;
  };
  spotify_data: {
    id: string;
    display_name: string;
    followers: number | { total: number };
    images: Array<{ url: string }>;
    country: string;
    product: string;
  };
}

interface SpotifyError {
  error: string;
  supabase_user?: any;
  link_spotify_url?: string;
}

export default function SpotifyDashboard() {
  const { user, loading: authLoading } = useAuth();
  const spotifyService = useAuthenticatedSpotifyService();
  
  // Helper function to safely render follower count
  const getFollowerCount = (followers: number | { total: number } | undefined): number => {
    if (typeof followers === 'number') return followers;
    if (typeof followers === 'object' && followers?.total) return followers.total;
    return 0;
  };

  // Helper function to safely render track count
  const getTrackCount = (tracks: any): string => {
    if (typeof tracks === 'object' && tracks?.total) return `${tracks.total} tracks`;
    if (typeof tracks === 'number') return `${tracks} tracks`;
    return 'Unknown tracks';
  };

  const [profile, setProfile] = useState<SpotifyProfile | null>(null);
  const [topTracks, setTopTracks] = useState<any[]>([]);
  const [playlists, setPlaylists] = useState<any[]>([]);
  const [currentlyPlaying, setCurrentlyPlaying] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [spotifyLinkId, setSpotifyLinkId] = useState("");

  useEffect(() => {
    if (user && !authLoading) {
      loadProfile();
    }
  }, [user, authLoading]);

  const loadProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const profileData = await spotifyService.getProfile();
      setProfile(profileData);
      
      // If profile loaded successfully, load other data
      await Promise.all([
        loadTopTracks(),
        loadPlaylists(),
        loadCurrentlyPlaying()
      ]);
    } catch (err: any) {
      setError(err.message);
      console.error("Error loading profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadTopTracks = async () => {
    try {
      const data = await spotifyService.getTopTracks();
      setTopTracks(data.top_tracks || []);
    } catch (err: any) {
      console.error("Error loading top tracks:", err);
    }
  };

  const loadPlaylists = async () => {
    try {
      const data = await spotifyService.getPlaylists();
      setPlaylists(data.playlists || []);
    } catch (err: any) {
      console.error("Error loading playlists:", err);
    }
  };

  const loadCurrentlyPlaying = async () => {
    try {
      const data = await spotifyService.getCurrentlyPlaying();
      setCurrentlyPlaying(data.currently_playing || null);
    } catch (err: any) {
      console.error("Error loading currently playing:", err);
    }
  };

  const handleLinkSpotify = async () => {
    if (!spotifyLinkId.trim()) {
      setError("Please enter a Spotify ID");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await spotifyService.linkSpotifyAccount(spotifyLinkId.trim());
      setSpotifyLinkId("");
      // Reload profile after linking
      await loadProfile();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
    return <div className="p-4">Loading authentication...</div>;
  }

  if (!user) {
    return <div className="p-4">Please log in to view your Spotify data.</div>;
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Spotify Dashboard</h1>
      
      {loading && <div className="text-blue-500 mb-4">Loading...</div>}
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
          {error.includes("not linked") && (
            <div className="mt-4">
              <h3 className="font-semibold mb-2">Link your Spotify account:</h3>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={spotifyLinkId}
                  onChange={(e) => setSpotifyLinkId(e.target.value)}
                  placeholder="Enter your Spotify ID"
                  className="flex-1 px-3 py-2 border rounded"
                />
                <button
                  onClick={handleLinkSpotify}
                  disabled={loading}
                  className="px-4 py-2 bg-green-500 text-white rounded disabled:opacity-50"
                >
                  Link Account
                </button>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                You can find your Spotify ID by going to your Spotify profile and copying the ID from the URL.
              </p>
            </div>
          )}
        </div>
      )}

      {profile && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">Profile</h2>
          <div className="flex items-center gap-4">
            {profile.spotify_data.images?.[0] && (
              <img 
                src={profile.spotify_data.images[0].url} 
                alt="Profile" 
                className="w-16 h-16 rounded-full"              />
            )}
            <div>
              <h3 className="text-xl font-semibold">{profile.spotify_data.display_name}</h3>
              <p className="text-gray-600">
                Followers: {getFollowerCount(profile.spotify_data.followers)}
              </p>
              <p className="text-gray-600">Country: {profile.spotify_data.country}</p>
              <p className="text-gray-600">Product: {profile.spotify_data.product}</p>
            </div>
          </div>
        </div>
      )}

      {currentlyPlaying && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">Currently Playing</h2>
          <div className="flex items-center gap-4">
            {currentlyPlaying.item?.album?.images?.[0] && (
              <img 
                src={currentlyPlaying.item.album.images[0].url} 
                alt="Album cover" 
                className="w-16 h-16 rounded"
              />
            )}
            <div>
              <h3 className="text-lg font-semibold">{currentlyPlaying.item?.name}</h3>
              <p className="text-gray-600">
                {currentlyPlaying.item?.artists?.map((artist: any) => artist.name).join(", ")}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">Top Tracks</h2>
          <div className="space-y-2">
            {topTracks.slice(0, 5).map((track, index) => (
              <div key={track.id} className="flex items-center gap-3">
                <span className="text-gray-500 w-6">{index + 1}</span>
                <div className="flex-1">
                  <p className="font-medium">{track.name}</p>
                  <p className="text-sm text-gray-600">
                    {track.artists?.map((artist: any) => artist.name).join(", ")}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold mb-4">Playlists</h2>
          <div className="space-y-2">
            {playlists.slice(0, 5).map((playlist) => (
              <div key={playlist.id} className="flex items-center gap-3">
                {playlist.images?.[0] && (
                  <img 
                    src={playlist.images[0].url} 
                    alt="Playlist cover" 
                    className="w-10 h-10 rounded"
                  />
                )}                <div className="flex-1">
                  <p className="font-medium">{playlist.name}</p>
                  <p className="text-sm text-gray-600">
                    {getTrackCount(playlist.tracks)}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
