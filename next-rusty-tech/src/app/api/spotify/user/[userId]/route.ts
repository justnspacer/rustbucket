// Example API route for user profile
import { NextRequest, NextResponse } from 'next/server';
import { SpotifyUserProfileResponse } from '@/types/spotify';

export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    const { userId } = params;
    
    if (!userId) {
      return NextResponse.json(
        { error: 'User ID is required' },
        { status: 400 }
      );
    }

    // This would call your Python backend through gatekeeper
    const response = await fetch(
      `${process.env.GATEKEEPER_URL || 'http://localhost:8000'}/api/spotify/user/${userId}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.API_KEY}`,
        },
      }
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }
    
    const data: SpotifyUserProfileResponse = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching user profile:', error);
    return NextResponse.json(
      { error: 'Failed to fetch user profile' },
      { status: 500 }
    );
  }
}
