'use client';
import { useAuth } from '@/app/context/AuthContext';
import SpotifyDashboard from '@/components/spotify/Dashboard';
import SpotifyLayout from '@/components/spotify/Layout';
import SpotifySearch from '@/components/spotify/Search';
import { useState, useEffect } from 'react';
import { setupIntersectionAnimations } from '@/hooks/useIntersectionAnimation';
import '@/styles/globals.css';

export default function SpotifyPage() {
  const { user, loading } = useAuth();

  useEffect(() => {
    setupIntersectionAnimations();
  }, []);

  if (loading) {
    return (
      <div className="content">
        <div>Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="content">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Welcome to Spotify Dashboard</h1>
          <p className="text-gray-600 mb-4">
            Please log in to access your Spotify data.
          </p>
          <a
            href="/auth/login">
            Go to Login
          </a>
        </div>
      </div>
    );
  }

  return (
    <SpotifyLayout>
      <SpotifyDashboard />
    </SpotifyLayout>
  );
}
