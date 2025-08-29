'use client';

import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

interface SpotifyUser {
  spotify_id: string;
  display_name: string;
  images?: Array<{ url: string }>;
  followers: number;
  country?: string;
  last_updated: string;
}

interface SpotifySearchResults {
  users: SpotifyUser[];
}

interface SpotifySearchProps {
  onUserSelect?: (userId: string) => void;
  className?: string;
}

export default function SpotifySearch({ onUserSelect, className = '' }: SpotifySearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SpotifyUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [allUsers, setAllUsers] = useState<SpotifyUser[]>([]);

  // Load all users on component mount
  useEffect(() => {
    loadAllUsers();
  }, []);

  const loadAllUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/spotify/users');
      const data: SpotifySearchResults = await response.json();
      
      if (data.users && data.users.length > 0) {
        setAllUsers(data.users);
        setResults(data.users);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.error('Error loading users:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const searchUsers = async () => {
    if (!query.trim()) {
      setResults(allUsers);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `/api/spotify/search-users?q=${encodeURIComponent(query)}`
      );
      const data: SpotifySearchResults = await response.json();

      if (data.users && data.users.length > 0) {
        setResults(data.users);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.error('Error searching users:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    searchUsers();
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      searchUsers();
    }
  };

  const handleUserClick = (userId: string) => {
    if (onUserSelect) {
      onUserSelect(userId);
    } else {
      // Default behavior - navigate to user profile
      window.location.href = `/spotify/user/${userId}`;
    }
  };

  return (
    <div className={`${className}`}>
      {/* Header */}
      <div className="">
        <h1 className="">
          Welcome to Spotify App
        </h1>
        <p className="">Search Spotify Users</p>
      </div>

      {/* Search Container */}
      <div className="search-container">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-box"
            placeholder="Search by username or Spotify ID..."
          />
          <button
            type="submit"
            disabled={loading}
            className="search-btn"
          >
            <FontAwesomeIcon icon={faSearch} className="mr-2" />
            Search
          </button>
        </form>
      </div>

      {/* Results */}
      <div id="results">
        {loading ? (
          <div>
            {query ? 'Searching...' : 'Loading users...'}
          </div>
        ) : results.length > 0 ? (
          <div>
            {results.map((user) => (
              <div
                key={user.spotify_id}
                className="user-card"
                onClick={() => handleUserClick(user.spotify_id)}
              >
                <img
                  src={
                    user.images && user.images.length > 0
                      ? user.images[0].url
                      : '/default-avatar.png'
                  }
                  alt={user.display_name || user.spotify_id}
                  className="user-avatar"
                />
                <div className="user-info">
                  <h3>
                    {user.display_name || user.spotify_id}
                  </h3>
                  <p>
                    Followers: {user.followers || 0} | Country: {user.country || 'N/A'}
                  </p>
                  <p>
                    Last updated: {new Date(user.last_updated).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div>
            {query 
              ? 'No users found.' 
              : 'No users found. Users need to authorize the app first.'
            }
          </div>
        )}
      </div>
    </div>
  );
}
