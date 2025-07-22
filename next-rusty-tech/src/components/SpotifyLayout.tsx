'use client';

import React from 'react';
import Link from 'next/link';

interface SpotifyLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export default function SpotifyLayout({ children, className = '' }: SpotifyLayoutProps) {
  return (
    <div className={`min-h-screen bg-gray-50 spotify-font ${className}`}>
      {/* Navigation */}
      <nav className="bg-gray-800 text-white p-4 text-xl font-light">
        <div className="max-w-6xl mx-auto flex gap-6">
          <Link 
            href="/spotify" 
            className="text-white hover:text-green-400 transition-colors"
          >
            Spotify UI
          </Link>
          <Link 
            href="/spotify/auth/link" 
            className="text-white hover:text-green-400 transition-colors"
          >
            Save My Profile
          </Link>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto p-8">
        {children}
      </main>
    </div>
  );
}
