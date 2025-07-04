from dotenv import load_dotenv
from rich.prompt import Prompt
import os

load_dotenv()

class Settings:
    def __init__(self):
        self.OPENAI_API_KEY = self._get_env_or_prompt("OPENAI_API_KEY", "🔑 Enter your OpenAI API Key")
        self.ANTHROPIC_API_KEY = self._get_env_or_prompt("ANTHROPIC_API_KEY", "🔑 Enter your Anthropic API Key")
        self.GOOGLE_API_KEY = self._get_env_or_prompt("GOOGLE_API_KEY", "🔑 Enter your Google API Key")
        self.GROQ_API_KEY = self._get_env_or_prompt("GROQ_API_KEY", "🔑 Enter your Groq API Key")

        # Optional values with defaults
        self.DB_PATH = os.getenv("DB_PATH", "conversation.db")
        self.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
        self.DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-qwq-32b")

    def _get_env_or_prompt(self, key: str, prompt_text: str) -> str:
        value = os.getenv(key)
        if not value:
            value = Prompt.ask(prompt_text, default="")
            if value:
                # Optional: save to .env file dynamically
                with open(".env", "a") as f:
                    f.write(f"{key}={value}\n")
        return value

settings = Settings()
