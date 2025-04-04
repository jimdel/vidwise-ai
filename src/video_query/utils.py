import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

def check_api_key():
    """Check if OpenAI API key is set and valid."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set it in your .env file:\n"
            "1. Create a .env file in the project root\n"
            "2. Add: OPENAI_API_KEY=your_api_key_here\n"
            "3. Replace 'your_api_key_here' with your actual OpenAI API key"
        )
    
    # Log the API key being used (with sensitive parts masked)
    masked_key = api_key[:7] + '*' * (len(api_key) - 10) + api_key[-3:]
    logger.info(f"Using OpenAI API key: {masked_key}")
    
    return api_key