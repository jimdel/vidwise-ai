import os
import logging
import time
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from openai import RateLimitError, APIConnectionError, AuthenticationError
from .utils import check_api_key
# Set up logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class PodcastKnowledgeBase:
    def __init__(self, persist_directory: str = "chroma_db"):
        """Initialize the knowledge base with a persistent storage directory."""
        self.persist_directory = persist_directory
        # Check API key before initializing
        check_api_key()
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def build_knowledge_base(self, transcripts_dir: str = "transcripts", max_retries: int = 3) -> None:
        """Build the knowledge base from transcript files."""
        try:
            # Get all transcript files
            transcript_files = [
                os.path.join(transcripts_dir, f) 
                for f in os.listdir(transcripts_dir) 
                if f.endswith('.txt')
            ]
            
            if not transcript_files:
                raise ValueError(f"No transcript files found in {transcripts_dir}")

            # Read and combine all transcripts
            all_text = ""
            for file_path in transcript_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    all_text += f.read() + "\n\n"

            # Split text into smaller chunks to reduce API usage
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,  # Reduced from 1000 to 500
                chunk_overlap=100  # Reduced from 200 to 100
            )
            texts = text_splitter.split_text(all_text)
            
            logger.info(f"Split text into {len(texts)} chunks")

            # Create vector store with retry logic
            for attempt in range(max_retries):
                try:
                    # Process chunks in smaller batches
                    batch_size = 10
                    for i in range(0, len(texts), batch_size):
                        batch = texts[i:i + batch_size]
                        logger.info(f"Processing batch {i//batch_size + 1}/{(len(texts) + batch_size - 1)//batch_size}")
                        
                        if i == 0:
                            self.vectorstore = Chroma.from_texts(
                                texts=batch,
                                embedding=self.embeddings,
                                persist_directory=self.persist_directory
                            )
                        else:
                            self.vectorstore.add_texts(batch)
                        
                        # Small delay between batches to avoid rate limits
                        time.sleep(1)
                    
                    self.vectorstore.persist()
                    break
                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 10  # Increased base wait time
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before retry...")
                        logger.warning("You may need to check your OpenAI account billing status at https://platform.openai.com/account/billing")
                        time.sleep(wait_time)
                        continue
                    raise
                except AuthenticationError as e:
                    logger.error("Authentication error. Please check your OpenAI API key.")
                    raise
                except APIConnectionError as e:
                    logger.error("Connection error. Please check your internet connection.")
                    raise
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    raise

            # Create QA chain
            llm = ChatOpenAI(temperature=0)
            self.qa_chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=self.vectorstore.as_retriever(),
                memory=self.memory
            )

            logger.info(f"Knowledge base built successfully with {len(transcript_files)} transcripts")

        except Exception as e:
            logger.error(f"Error building knowledge base: {str(e)}")
            raise

    def query(self, question: str, max_retries: int = 3) -> str:
        """Query the knowledge base with a question."""
        if not self.qa_chain:
            raise ValueError("Knowledge base not built. Call build_knowledge_base() first.")

        for attempt in range(max_retries):
            try:
                result = self.qa_chain({"question": question})
                return result["answer"]
            except RateLimitError as e:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 10  # Increased base wait time
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before retry...")
                    logger.warning("You may need to check your OpenAI account billing status at https://platform.openai.com/account/billing")
                    time.sleep(wait_time)
                    continue
                raise
            except AuthenticationError as e:
                logger.error("Authentication error. Please check your OpenAI API key.")
                raise
            except APIConnectionError as e:
                logger.error("Connection error. Please check your internet connection.")
                raise
            except Exception as e:
                logger.error(f"Error querying knowledge base: {str(e)}")
                raise

    def get_chat_history(self) -> List[Dict[str, str]]:
        """Get the conversation history."""
        if not self.memory:
            return []
        return self.memory.chat_memory.messages

def create_knowledge_base(transcripts_dir: str = "transcripts") -> PodcastKnowledgeBase:
    """Create and return a new knowledge base instance."""
    kb = PodcastKnowledgeBase()
    kb.build_knowledge_base(transcripts_dir)
    return kb

def query_interface(kb):
    """Interactive query interface for the knowledge base."""
    print("\nWelcome to the Podcast Knowledge Base!")
    print("Type 'exit' to quit or 'history' to see conversation history.")
    
    while True:
        question = input("\nWhat would you like to know? ")
        
        if question.lower() == 'exit':
            break
        elif question.lower() == 'history':
            history = kb.get_chat_history()
            for msg in history:
                print(f"\n{msg.type}: {msg.content}")
            continue
            
        try:
            answer = kb.query(question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"\nError: {str(e)}")