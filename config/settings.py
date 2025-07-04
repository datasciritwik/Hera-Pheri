from dotenv import load_dotenv
from rich.prompt import Prompt
import os
import sys

load_dotenv()

class Settings:
    def __init__(self):
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

        # Prompt for mandatory keys if missing
        if not self.TAVILY_API_KEY:
            self.TAVILY_API_KEY = self._prompt_key("TAVILY_API_KEY", "🔑 Enter your Tavily API Key (mandatory)")

        if not any([self.OPENAI_API_KEY, self.ANTHROPIC_API_KEY, self.GOOGLE_API_KEY, self.GROQ_API_KEY]):
            self._prompt_one_llm_key()

        # Defaults
        self.DB_PATH = os.getenv("DB_PATH", "conversation.db")
        self.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
        self.DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "qwen-qwq-32b")

    def _prompt_key(self, env_var: str, prompt_text: str) -> str:
        if not sys.stdin.isatty():
            print(f"❌ Missing required environment variable: {env_var} and no interactive input possible.")
            sys.exit(1)
        key = None
        while not key:
            key = Prompt.ask(prompt_text).strip()
            if not key:
                print("⚠️ This value is required.")
        # Save to .env for future runs
        with open(".env", "a") as f:
            f.write(f"{env_var}={key}\n")
        return key

    def _prompt_one_llm_key(self):
        if not sys.stdin.isatty():
            print("❌ Missing all LLM API keys and no interactive input possible.")
            sys.exit(1)

        print("⚠️ No LLM API keys found. Please enter at least one to continue.")

        choices = {
            "openai": "🔑 OpenAI API Key",
            "anthropic": "🔑 Anthropic API Key",
            "google": "🔑 Google API Key",
            "groq": "🔑 Groq API Key",
        }

        provider = None
        while provider not in choices:
            provider = Prompt.ask("Which LLM provider do you want to configure?", choices=list(choices.keys()))

        key = None
        while not key:
            key = Prompt.ask(choices[provider]).strip()
            if not key:
                print("⚠️ This value is required.")

        env_key_map = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "groq": "GROQ_API_KEY",
        }

        env_var = env_key_map[provider]
        setattr(self, env_var, key)

        # Save to .env
        with open(".env", "a") as f:
            f.write(f"{env_var}={key}\n")

settings = Settings()
