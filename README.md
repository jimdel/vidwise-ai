# VideoQuery

A tool that uses LLM technology to search through a video's audio content. This project enables a user to download YouTube videos, transcribe them, and create a searchable knowledge base using OpenAI's API.

## How It Works

- Download audio from YouTube videos using `yt-dlp`
- Transcribe audio using OpenAI's Whisper
- Create a searchable knowledge base with the transcriptions using LangChain and ChromaDB
- Start an interactive query interface to chat with the knowledge base
- Maintains conversation history for context-aware answers

### Detailed Steps

1. **Audio Download**

   - Uses `yt-dlp` to download audio from YouTube videos
   - Converts audio to MP3 format
   - Saves files in the `audio` directory

2. **Transcription**

   - Uses OpenAI's Whisper model to transcribe the audio with either CPU or GPU processing (if available)
   - Saves transcripts in the `transcripts` directory

3. **Create a Knowledge Base**

   - Creates embeddings using OpenAI's API
   - Stores vectors in ChromaDB for efficient similarity search
   - Splits transcripts into chunks for better context handling
   - Maintains conversation history for context-aware answers

4. **Query Interface**
   - Interactive command-line interface
   - Supports natural language questions
   - Shows conversation history
   - Provides relevant answers based on the content

## Requirements

- Python 3.9 or higher
- FFmpeg (for audio processing)
- OpenAI API key

## Installation

1. Install dependencies:

```bash
poetry install
```

2. Install `FFmpeg`:

```bash
# On macOS
brew install ffmpeg

# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On Windows (using Chocolatey)
choco install ffmpeg
```

3. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

```bash
poetry run python -m src.podcast_searcher.main
```

## Future Ideas

- Create an MCP server that can be used by other services to search through podcast audio.
- Use cases:
  - Search through YouTube courses, generate a knowledge base, and use it to answer questions about the course.
