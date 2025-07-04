import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Database 
    DB_PATH = os.getenv("DB_PATH", "conversation.db")
    
    # Default settings
    DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-qwq-32b")
    
    
settings = Settings()