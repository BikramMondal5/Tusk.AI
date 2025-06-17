import { NextRequest, NextResponse } from 'next/server';
import { YoutubeTranscript } from 'youtube-transcript';

export async function POST(request: NextRequest) {
  try {
    const { videoUrl } = await request.json();
    
    if (!videoUrl) {
      return NextResponse.json({ error: 'Video URL is required' }, { status: 400 });
    }

    // Extract video ID from URL
    let videoId;
    try {
      const url = new URL(videoUrl);
      if (url.hostname === 'youtu.be') {
        // Short youtu.be links
        videoId = url.pathname.substring(1);
      } else if (url.hostname === 'www.youtube.com' || url.hostname === 'youtube.com') {
        // Regular youtube.com links
        const params = new URLSearchParams(url.search);
        videoId = params.get('v');
      }
    } catch (error) {
      console.error('Error parsing YouTube URL:', error);
      return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
    }

    if (!videoId) {
      return NextResponse.json({ error: 'Could not extract video ID from URL' }, { status: 400 });
    }

    console.log(`Fetching transcript for video ID: ${videoId}`);
    
    const transcript = await YoutubeTranscript.fetchTranscript(videoId);
    
    console.log('Transcript fetched successfully:', transcript);
    
    return NextResponse.json({ transcript });
  } catch (error: any) {
    console.error('Error fetching transcript:', error);
    
    // Handle case when no transcript is available
    if (error.message && error.message.includes('Could not get transcripts for video')) {
      return NextResponse.json(
        { error: 'No transcript available for this video' }, 
        { status: 404 }
      );
    }
    
    return NextResponse.json(
      { error: error.message || 'Failed to fetch transcript' }, 
      { status: 500 }
    );
  }
}