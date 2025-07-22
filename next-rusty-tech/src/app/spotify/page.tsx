"use client";
import { useAuth } from "@/app/context/AuthContext";
import SpotifyDashboardSafe from "@/components/SpotifyDashboardSafe";
import SpotifyConnectionTest from "@/components/SpotifyConnectionTest";
import SpotifyLayout from "@/components/SpotifyLayout";
import SpotifySearch from "@/components/SpotifySearch";
import { useState, useEffect } from "react";
import { setupIntersectionAnimations } from "@/hooks/useIntersectionAnimation";
import "@/styles/spotify.css";

export default function SpotifyPage() {
  const { user, loading } = useAuth();
  const [showTest, setShowTest] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  useEffect(() => {
    // Initialize animations when the page loads
    setupIntersectionAnimations();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Authentication Required</h1>
          <p className="text-gray-600 mb-4">Please log in to access your Spotify data.</p>
          <a 
            href="/login" 
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Go to Login
          </a>
        </div>
      </div>
    );
  }
  return (
    <SpotifyLayout>
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">Spotify Integration</h1>
          <div className="space-x-2">
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              {showSearch ? 'Hide Search' : 'Show User Search'}
            </button>
            <button
              onClick={() => setShowTest(!showTest)}
              className="bg-gray-500 text-white px-3 py-1 rounded text-sm hover:bg-gray-600"
            >
              {showTest ? 'Hide Test' : 'Show Connection Test'}
            </button>
          </div>
        </div>
        
        {showSearch && (
          <div className="bg-white p-6 rounded-lg shadow">
            <SpotifySearch />
          </div>
        )}
        
        {showTest && <SpotifyConnectionTest />}
        
        <SpotifyDashboardSafe />
      </div>
    </SpotifyLayout>
  );
}
