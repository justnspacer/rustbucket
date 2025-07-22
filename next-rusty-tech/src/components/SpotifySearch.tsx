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
    <div className={`spotify-font ${className}`}>
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-4 text-gray-800">
          Welcome to Spotify App
        </h1>
        <p className="text-gray-600">Search Spotify Users</p>
      </div>

      {/* Search Container */}
      <div className="bg-white p-5 rounded-lg shadow-md mb-5">
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
            className="flex-1 p-3 border border-gray-300 rounded-md text-base font-medium bg-gray-800 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Search by username or Spotify ID..."
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-3 rounded-md font-medium transition-colors disabled:opacity-50"
          >
            <FontAwesomeIcon icon={faSearch} className="mr-2" />
            Search
          </button>
        </form>
      </div>

      {/* Results */}
      <div id="results">
        {loading ? (
          <div className="text-center py-5 text-gray-600">
            {query ? 'Searching...' : 'Loading users...'}
          </div>
        ) : results.length > 0 ? (
          <div className="space-y-3">
            {results.map((user) => (
              <div
                key={user.spotify_id}
                className="bg-white p-4 rounded-lg shadow-md flex items-center cursor-pointer hover:shadow-lg transition-shadow"
                onClick={() => handleUserClick(user.spotify_id)}
              >
                <img
                  src={
                    user.images && user.images.length > 0
                      ? user.images[0].url
                      : '/default-avatar.png'
                  }
                  alt={user.display_name || user.spotify_id}
                  className="user-avatar mr-4 bg-gray-200"
                />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-800 mb-1">
                    {user.display_name || user.spotify_id}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    Followers: {user.followers || 0} | Country: {user.country || 'N/A'}
                  </p>
                  <p className="text-gray-500 text-xs">
                    Last updated: {new Date(user.last_updated).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-5 text-gray-600">
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
