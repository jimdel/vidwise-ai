import whisper
import logging
import os
import torch
from dotenv import load_dotenv

load_dotenv()
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Set up logging
logger = logging.getLogger(__name__)

def transcribe_audio(audio_file: str) -> str:
    """Transcribe audio file using Whisper."""
    try:
        logger.info("Loading Whisper model...")
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        model = whisper.load_model(WHISPER_MODEL, device=device)
        
        logger.info("Starting transcription...")
        result = model.transcribe(audio_file)
        transcript = result["text"]
        logger.info("Transcription completed successfully")
        return transcript
        
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise

def write_transcript_to_file(transcript: str, audio_file: str) -> str:
    """Write transcript to a file and return the path."""
    os.makedirs('transcripts', exist_ok=True)
    transcript_file = os.path.join('transcripts', f"{os.path.basename(audio_file)[:-4]}.txt")
    with open(transcript_file, 'w', encoding='utf-8') as f:
        f.write(transcript)
    logger.info(f"Transcript written to: {transcript_file}")
    return transcript_file 