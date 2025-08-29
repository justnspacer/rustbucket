'use client';

import React, { useEffect } from 'react';
import { useParams } from 'next/navigation';
import SpotifyLayout from '@/components/spotify/SpotifyLayout';
import SpotifyUserProfile from '@/components/spotify/SpotifyUserProfile';
import { setupIntersectionAnimations } from '@/hooks/useIntersectionAnimation';
import '@/styles/spotify.css';

export default function SpotifyPublicUserPage() {
  const params = useParams();
  const userId = params.userId as string;

  useEffect(() => {
    // Initialize animations when the page loads
    setupIntersectionAnimations();
  }, []);

  if (!userId) {
    return (
      <SpotifyLayout>
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold mb-4">User Not Found</h1>
          <p className="text-gray-600">Invalid user ID provided.</p>
        </div>
      </SpotifyLayout>
    );
  }

  return (
    <SpotifyLayout>
      <SpotifyUserProfile userId={userId} isPublic={true} />
    </SpotifyLayout>
  );
}
