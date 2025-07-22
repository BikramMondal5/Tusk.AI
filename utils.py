import os
import pytube
import moviepy.editor as mp
import re
import sys
from pytube.exceptions import RegexMatchError, VideoUnavailable

# Add SoniTranslate to path for using its utilities
sys.path.append(os.path.join(os.path.dirname(__file__), "SoniTranslate"))

# Try to import SoniTranslate's YouTube download utility as a fallback
try:
    from SoniTranslate.soni_translate.utils import run_command
    SONI_AVAILABLE = True
except ImportError:
    SONI_AVAILABLE = False

def sanitize_filename(filename):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_video(youtube_url, output_dir):
    """
    Download a YouTube video.
    
    Args:
        youtube_url: URL of the YouTube video
        output_dir: Directory to save the video
        
    Returns:
        Path to the downloaded video file
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # First attempt with pytube
        try:
            # Create a YouTube object
            yt = pytube.YouTube(youtube_url)
            
            # Get video title and sanitize for filename
            video_title = sanitize_filename(yt.title)
            if not video_title:
                video_title = "downloaded_video"
            
            # Get the highest resolution stream
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            
            # If no suitable stream is found, try without progressive filter
            if not video_stream:
                video_stream = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
            
            # If still no suitable stream, raise an error
            if not video_stream:
                raise Exception("No suitable video stream found")
                
            # Download the video
            print(f"Downloading: {video_title}")
            video_path = video_stream.download(output_path=output_dir, filename=f"{video_title}.mp4")
            
            print(f"Downloaded to: {video_path}")
            return video_path
            
        except (RegexMatchError, VideoUnavailable) as e:
            print(f"Pytube error: {e}. Trying alternative method...")
            if not SONI_AVAILABLE:
                raise
                
            # Use SoniTranslate's method (yt-dlp) as a fallback
            output_path = os.path.join(output_dir, "downloaded_video.mp4")
            command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" "{youtube_url}" -o "{output_path}"'
            run_command(command)
            
            if os.path.exists(output_path):
                print(f"Downloaded to: {output_path}")
                return output_path
            else:
                raise Exception("Failed to download video with both methods")
    
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        raise

def process_audio(video_path):
    """
    Extract audio from video file.
    
    Args:
        video_path: Path to the video file
        
    Returns:
        Path to the extracted audio file
    """
    try:
        # Get the directory and filename without extension
        dir_path = os.path.dirname(video_path)
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(dir_path, f"{base_name}.wav")
        
        # Load the video file
        video = mp.VideoFileClip(video_path)
        
        # Extract the audio
        audio = video.audio
        audio.write_audiofile(audio_path)
        
        # Close the video clip to free resources
        video.close()
        
        print(f"Audio extracted to: {audio_path}")
        return audio_path
    
    except Exception as e:
        print(f"Error processing audio: {e}")
        raise

def detect_language(audio_path):
    """
    Detect the language of the audio.
    This is a placeholder function that would use a real model.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Detected language code
    """
    # In a real implementation, this would use a language detection model
    # For example:
    # from speechbrain.pretrained import EncoderClassifier
    # classifier = EncoderClassifier.from_hparams("speechbrain/lang-id-voxlingua107-ecapa")
    # lang_id = classifier.classify_file(audio_path)
    
    print(f"Detecting language from: {audio_path}")
    # Placeholder for demo purposes
    return "en"  # Default to English