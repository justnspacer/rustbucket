// Example API route for searching users
import { NextRequest, NextResponse } from 'next/server';
import { SpotifySearchResponse } from '@/types/spotify';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q');
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter is required' },
        { status: 400 }
      );
    }
    
    // This would call your Python backend
    const response = await fetch(
      `http://127.0.0.1:5000/spotify/search-users?q=${encodeURIComponent(query)}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.API_KEY}`,
        },
      }
    );
    if (!response.ok) {
      throw new Error('Failed to search users');
    }
    
    const data: SpotifySearchResponse = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error searching users:', error);
    return NextResponse.json(
      { error: 'Failed to search users' },
      { status: 500 }
    );
  }
}
