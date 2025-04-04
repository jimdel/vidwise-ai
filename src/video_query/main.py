import logging
from .process_video import process_video
from .knowledge_base import create_knowledge_base
from .knowledge_base import query_interface

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Example usage
    video_url = "https://www.youtube.com/watch?v=RgR1C6VAqQQ"

    try:
        # Process the video
        transcript_file = process_video(video_url)
        logger.info(f"\nTranscript written to: {transcript_file}")

    
        # Create and use the knowledge base
        logger.info("\nBuilding knowledge base...")
        kb = create_knowledge_base()
        
        # Start the query interface
        query_interface(kb)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
