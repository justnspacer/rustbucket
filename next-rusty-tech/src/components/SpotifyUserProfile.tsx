'use client';

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeadphones, faTimes } from '@fortawesome/free-solid-svg-icons';

interface SpotifyImage {
  url: string;
  height?: number;
  width?: number;
}

interface SpotifyFollowers {
  total: number;
}

interface SpotifyExternalUrls {
  spotify: string;
}

interface SpotifyUser {
  id: string;
  spotify_id: string;
  display_name: string;
  images?: SpotifyImage[];
  followers: SpotifyFollowers | number;
  country?: string;
  product?: string;
  last_updated?: string;
  external_urls?: SpotifyExternalUrls;
}

interface SpotifyArtist {
  id: string;
  name: string;
  images?: SpotifyImage[];
  popularity?: number;
  external_urls?: SpotifyExternalUrls;
}

interface SpotifyTrack {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  album: {
    id: string;
    name: string;
    images?: SpotifyImage[];
  };
  popularity?: number;
  added_at?: string;
  external_urls?: SpotifyExternalUrls;
}

interface SpotifyPlaylist {
  id: string;
  name: string;
  description?: string;
  images?: SpotifyImage[];
  tracks: {
    total: number;
  };
  public?: boolean;
  external_urls?: SpotifyExternalUrls;
}

interface CurrentlyPlaying {
  item: SpotifyTrack;
  is_playing: boolean;
  progress_ms: number;
}

interface SpotifyUserProfileProps {
  userId: string;
  isPublic?: boolean;
  className?: string;
}

interface ModalData {
  title: string;
  content: any;
  type: 'artist' | 'track' | 'playlist';
}

export default function SpotifyUserProfile({ 
  userId, 
  isPublic = false, 
  className = '' 
}: SpotifyUserProfileProps) {
  const [user, setUser] = useState<SpotifyUser | null>(null);
  const [topArtists, setTopArtists] = useState<SpotifyArtist[]>([]);
  const [topTracks, setTopTracks] = useState<SpotifyTrack[]>([]);
  const [playlists, setPlaylists] = useState<SpotifyPlaylist[]>([]);
  const [savedTracks, setSavedTracks] = useState<SpotifyTrack[]>([]);
  const [currentlyPlaying, setCurrentlyPlaying] = useState<CurrentlyPlaying | null>(null);
  const [loading, setLoading] = useState(true);
  const [modal, setModal] = useState<ModalData | null>(null);

  useEffect(() => {
    loadUserData();
    if (!isPublic) {
      loadUserContent();
      loadCurrentlyPlaying();
      // Set up interval for currently playing
      const interval = setInterval(loadCurrentlyPlaying, 30000);
      return () => clearInterval(interval);
    }
  }, [userId, isPublic]);

  const loadUserData = async () => {
    try {
      const response = await fetch(`/api/spotify/user/${userId}`);
      const userData = await response.json();
      setUser(userData);
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUserContent = async () => {
    try {
      const [artistsRes, tracksRes, playlistsRes, savedRes] = await Promise.all([
        fetch(`/api/spotify/user/${userId}/top-artists`),
        fetch(`/api/spotify/user/${userId}/top-tracks`),
        fetch(`/api/spotify/user/${userId}/playlists`),
        fetch(`/api/spotify/user/${userId}/saved-tracks`)
      ]);

      const [artists, tracks, playlists, saved] = await Promise.all([
        artistsRes.json(),
        tracksRes.json(),
        playlistsRes.json(),
        savedRes.json()
      ]);

      setTopArtists(artists.items || []);
      setTopTracks(tracks.items || []);
      setPlaylists(playlists.items || []);
      setSavedTracks(saved.items || []);
    } catch (error) {
      console.error('Error loading user content:', error);
    }
  };

  const loadCurrentlyPlaying = async () => {
    if (isPublic) return;
    
    try {
      const response = await fetch(`/api/spotify/user/${userId}/currently-playing`);
      if (response.ok) {
        const data = await response.json();
        setCurrentlyPlaying(data);
      }
    } catch (error) {
      console.error('Error loading currently playing:', error);
    }
  };

  const openModal = (title: string, content: any, type: 'artist' | 'track' | 'playlist') => {
    setModal({ title, content, type });
  };

  const closeModal = () => {
    setModal(null);
  };

  const getFollowerCount = (followers: SpotifyFollowers | number) => {
    if (typeof followers === 'number') return followers;
    return followers?.total || 0;
  };

  if (loading) {
    return (
      <div className={`spotify-font ${className} flex justify-center items-center min-h-64`}>
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className={`spotify-font ${className}`}>
        <div className="text-center py-12">
          <p className="text-gray-600">User not found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`spotify-font ${className}`}>
      {/* User Background/Header */}
      <div className="flex flex-col md:flex-row items-center justify-center gap-8 p-6 mb-8">
        <div className="animate animate-from-right">
          <img
            src={
              user.images && user.images.length > 0
                ? user.images[0].url
                : '/default-avatar.png'
            }
            alt={user.display_name || user.spotify_id}
            className="user-profile-image"
          />
        </div>
        <div className="animate animate-from-left text-center md:text-left">
          <h1 className="text-4xl font-bold mb-2 text-gray-800">
            {user.display_name || user.spotify_id}
            <FontAwesomeIcon icon={faHeadphones} className="ml-2 text-blue-500" />
          </h1>
          <p className="text-xl font-bold text-gray-600 mb-2">
            <span className="text-2xl">{getFollowerCount(user.followers)}</span> followers
          </p>
          <p className="text-gray-600">{user.id || user.spotify_id}</p>
          {isPublic && <p className="text-sm italic text-gray-500">Public Profile</p>}
        </div>
      </div>

      {/* Content Lists */}
      <div className="animate animate-from-center space-y-8">
        {/* Top Artists */}
        <div>
          <h2 className="text-2xl font-normal mb-4">
            {isPublic ? 'Top Artists' : 'Current Top Artists'}
          </h2>
          <div className="flex flex-wrap gap-4">
            {topArtists.slice(0, 10).map((artist) => (
              <div
                key={artist.id}
                className="w-40 h-40 rounded-full overflow-hidden cursor-pointer transform hover:scale-110 transition-transform"
                onClick={() => openModal(artist.name, artist, 'artist')}
              >
                <img
                  src={artist.images?.[0]?.url || '/default-avatar.png'}
                  alt={artist.name}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Top Tracks */}
        <div>
          <h2 className="text-2xl font-normal mb-4">
            {isPublic ? 'Top Tracks' : 'Latest Top Tracks'}
            <span className="text-sm ml-2">(popularity)</span>
          </h2>
          <div className="flex flex-wrap gap-4">
            {topTracks.slice(0, 20).map((track) => (
              <div
                key={track.id}
                className="list-item relative w-30 h-30 cursor-pointer"
                style={{
                  backgroundImage: `url(${track.album.images?.[0]?.url || '/default-album.png'})`
                }}
                onClick={() => openModal(track.name, track, 'track')}
              >
                <div className="list-item-content">
                  {track.popularity && (
                    <span className="popularity-badge">{track.popularity}</span>
                  )}
                  <div className="hidden hover:block text-center">
                    <p className="font-bold text-xs">{track.name}</p>
                    <p className="text-xs">{track.artists[0]?.name}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Playlists */}
        <div>
          <h2 className="text-2xl font-normal mb-4">
            {isPublic ? 'Public Playlists' : 'Shared Playlists'}
          </h2>
          <div className="flex flex-wrap gap-4">
            {playlists.slice(0, 10).map((playlist) => (
              <div
                key={playlist.id}
                className="list-item relative w-30 h-30 cursor-pointer"
                style={{
                  backgroundImage: `url(${playlist.images?.[0]?.url || '/default-playlist.png'})`
                }}
                onClick={() => openModal(playlist.name, playlist, 'playlist')}
              >
                <div className="list-item-content">
                  <div className="hidden hover:block text-center">
                    <p className="font-bold text-xs">{playlist.name}</p>
                    <p className="text-xs">{playlist.tracks.total} tracks</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Saved Tracks (only for non-public profiles) */}
        {!isPublic && (
          <div>
            <h2 className="text-2xl font-normal mb-4">
              Latest Saved Tracks <span className="text-sm">(date added)</span>
            </h2>
            <div className="flex flex-wrap gap-4">
              {savedTracks.slice(0, 20).map((track) => (
                <div
                  key={track.id}
                  className="list-item relative w-30 h-30 cursor-pointer"
                  style={{
                    backgroundImage: `url(${track.album.images?.[0]?.url || '/default-album.png'})`
                  }}
                  onClick={() => openModal(track.name, track, 'track')}
                >
                  <div className="list-item-content">
                    {track.added_at && (
                      <span className="item-added-badge">
                        {new Date(track.added_at).toLocaleDateString()}
                      </span>
                    )}
                    <div className="hidden hover:block text-center">
                      <p className="font-bold text-xs">{track.name}</p>
                      <p className="text-xs">{track.artists[0]?.name}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Public Profile Info */}
      {isPublic && (
        <div className="bg-white max-w-3xl mx-auto mt-8 p-5 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Profile Information</h2>
          <div className="bg-gray-100 p-4 rounded-md space-y-2">
            <p><strong className="text-green-600">Country:</strong> {user.country || 'Not specified'}</p>
            <p><strong className="text-green-600">Spotify Product:</strong> {user.product || 'Not specified'}</p>
            <p><strong className="text-green-600">Profile Last Updated:</strong> {user.last_updated || 'Unknown'}</p>
            {user.external_urls?.spotify && (
              <p>
                <a 
                  href={user.external_urls.spotify} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  View on Spotify
                </a>
              </p>
            )}
          </div>
          <p className="text-sm italic text-gray-600 mt-4">
            This is a public profile. Some information may be limited to protect user privacy.
          </p>
        </div>
      )}

      {/* Currently Playing */}
      {!isPublic && currentlyPlaying && (
        <div className="currently-playing-container">
          <div className="bg-gray-800 text-white p-4 rounded-lg">
            <h2 className="text-lg font-normal mb-2">Currently Playing</h2>
            <img
              src={currentlyPlaying.item.album.images?.[0]?.url || '/default-album.png'}
              alt={currentlyPlaying.item.name}
              className="w-full mb-2"
            />
            <div className="track-info">
              <p className="track-name font-normal text-center">
                {currentlyPlaying.item.name}
              </p>
              <p className="artist-line text-sm text-center">
                <span className="text-green-400">Artist:</span> {currentlyPlaying.item.artists[0]?.name}
              </p>
              <p className="album-line text-sm text-center">
                <span className="text-green-400">Album:</span> {currentlyPlaying.item.album.name}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {modal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="absolute top-4 right-4 text-2xl font-bold text-gray-800 hover:text-gray-600"
              onClick={closeModal}
            >
              <FontAwesomeIcon icon={faTimes} />
            </button>
            
            <h2 className="text-xl font-bold mb-4 text-gray-800">{modal.title}</h2>
            
            {modal.type === 'artist' && (
              <div>
                <img
                  src={modal.content.images?.[0]?.url || '/default-avatar.png'}
                  alt={modal.content.name}
                />
                <div className="space-y-2">
                  <p><strong>Name:</strong> {modal.content.name}</p>
                  <p><strong>Popularity:</strong> {modal.content.popularity || 'N/A'}</p>
                  {modal.content.external_urls?.spotify && (
                    <p>
                      <a
                        href={modal.content.external_urls.spotify}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        View on Spotify
                      </a>
                    </p>
                  )}
                </div>
              </div>
            )}
            
            {modal.type === 'track' && (
              <div>
                <img
                  src={modal.content.album.images?.[0]?.url || '/default-album.png'}
                  alt={modal.content.name}
                />
                <div className="space-y-2">
                  <p><strong>Track:</strong> {modal.content.name}</p>
                  <p><strong>Artist:</strong> {modal.content.artists[0]?.name}</p>
                  <p><strong>Album:</strong> {modal.content.album.name}</p>
                  <p><strong>Popularity:</strong> {modal.content.popularity || 'N/A'}</p>
                  {modal.content.added_at && (
                    <p><strong>Added:</strong> {new Date(modal.content.added_at).toLocaleDateString()}</p>
                  )}
                  {modal.content.external_urls?.spotify && (
                    <p>
                      <a
                        href={modal.content.external_urls.spotify}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        View on Spotify
                      </a>
                    </p>
                  )}
                </div>
              </div>
            )}
            
            {modal.type === 'playlist' && (
              <div>
                <img
                  src={modal.content.images?.[0]?.url || '/default-playlist.png'}
                  alt={modal.content.name}
                />
                <div className="space-y-2">
                  <p><strong>Playlist:</strong> {modal.content.name}</p>
                  {modal.content.description && (
                    <p><strong>Description:</strong> {modal.content.description}</p>
                  )}
                  <p><strong>Tracks:</strong> {modal.content.tracks.total}</p>
                  <p><strong>Public:</strong> {modal.content.public ? 'Yes' : 'No'}</p>
                  {modal.content.external_urls?.spotify && (
                    <p>
                      <a
                        href={modal.content.external_urls.spotify}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-500 hover:underline"
                      >
                        View on Spotify
                      </a>
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
