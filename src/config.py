import os
from dotenv import load_dotenv

# ==============================================================================
# LOAD ENVIRONMENT VARIABLES
# ==============================================================================

load_dotenv()

# ==============================================================================
# API KEYS AND VALIDATION
# ==============================================================================

# Fetch API keys from the environment.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


if not TAVILY_API_KEY:
    raise ValueError(
        "FATAL: TAVILY_API_KEY is not set in the environment or .env file. "
        "Please get a key from https://tavily.com/ and add it to your .env file."
    )


def init_config():
    """Load environment variables and validate required API keys."""
    from dotenv import load_dotenv
    import os
    load_dotenv()
    # Fetch API keys from the environment.
    groq_api_key = os.getenv("GROQ_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError(
            "FATAL: TAVILY_API_KEY is not set in the environment or .env file. "
            "Please get a key from https://tavily.com/ and add it to your .env file."
        )
    # Optionally, validate groq_api_key as well if needed
    return groq_api_key, tavily_api_key