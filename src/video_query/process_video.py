import yt_dlp
import logging
import time
import os
from typing import Optional
from .transcribe_audio import transcribe_audio, write_transcript_to_file

# Set up logging
logger = logging.getLogger(__name__)

# Create audio directory if it doesn't exist
AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def process_video(video_url: str) -> str:
    """Process a video URL and return the transcript file path."""
    try:
        audio_file = download_audio(video_url)
        if not audio_file:
            raise ValueError("Failed to download audio")
            
        transcript = transcribe_audio(audio_file)
        transcript_file = write_transcript_to_file(transcript, audio_file)
        return transcript_file
    except Exception as e:
        logger.error(f"Failed to process video: {str(e)}")
        raise

def download_audio(url: str, max_retries: int = 3) -> Optional[str]:
    """Download audio from YouTube with retry logic using yt-dlp."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(AUDIO_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to download audio from: {url} (attempt {attempt + 1}/{max_retries})")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info
                info = ydl.extract_info(url, download=False)
                logger.info(f"Video title: {info.get('title', 'Unknown')}")
                logger.info(f"Video duration: {info.get('duration', 'Unknown')} seconds")
                
                # Download the audio
                ydl.download([url])
                
                # Get the downloaded file path
                audio_file = os.path.join(AUDIO_DIR, f"{info['title']}.mp3")
                if os.path.exists(audio_file):
                    logger.info(f"Successfully downloaded audio to: {audio_file}")
                    return audio_file
                else:
                    raise Exception("Downloaded file not found")
                
        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            if attempt < max_retries - 1:
                logger.info("Retrying after a short delay...")
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
    
    return None 