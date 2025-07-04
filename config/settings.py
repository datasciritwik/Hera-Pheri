from dotenv import load_dotenv
from rich.prompt import Prompt
import os

load_dotenv()

class Settings:
    def __init__(self):
        # Load all keys from environment
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        # Ensure TAVILY_API_KEY is present, prompt if missing
        if not self.TAVILY_API_KEY:
            self.TAVILY_API_KEY = self._prompt_and_save("TAVILY_API_KEY", "🔑 Enter your Tavily API Key (mandatory)")

        # Ensure at least one LLM key is present, prompt for one if none
        if not any([self.OPENAI_API_KEY, self.ANTHROPIC_API_KEY, self.GOOGLE_API_KEY, self.GROQ_API_KEY]):
            self._prompt_one_llm_key()

        # Optional defaults
        self.DB_PATH = os.getenv("DB_PATH", "conversation.db")
        self.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
        self.DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-qwq-32b")

    def _prompt_and_save(self, env_key: str, prompt_text: str) -> str:
        key = Prompt.ask(prompt_text)
        # Save to .env
        with open(".env", "a") as f:
            f.write(f"{env_key}={key}\n")
        return key

    def _prompt_one_llm_key(self):
        print("⚠️ No LLM API keys found. Please enter at least one to continue.")

        choices = {
            "openai": "🔑 OpenAI API Key",
            "anthropic": "🔑 Anthropic API Key",
            "google": "🔑 Google API Key",
            "groq": "🔑 Groq API Key",
        }

        provider = Prompt.ask("Which LLM provider do you want to configure?", choices=list(choices.keys()))
        key = Prompt.ask(choices[provider])

        env_key_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "groq": "GROQ_API_KEY",
        }

        env_key = env_key_map[provider]

        # Save to .env file
        with open(".env", "a") as f:
            f.write(f"{env_key}={key}\n")

        setattr(self, env_key, key)


settings = Settings()
