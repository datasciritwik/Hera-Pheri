from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from config.settings import settings

class BaseLLMProvider(ABC):
    @abstractmethod
    def get_llm(self, model: str = "qwen-qwq-32b", temperature: float = 0.7):
        pass

class OpenAIProvider(BaseLLMProvider):
    def get_llm(self, model: str = "gpt-4", temperature: float = 0.7):
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature
        )

class AnthropicProvider(BaseLLMProvider):
    def get_llm(self, model: str = "claude-3-haiku-20240307", temperature: float = 0.7):
        return ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model=model,
            temperature=temperature
        )

class GoogleProvider(BaseLLMProvider):
    def get_llm(self, model: str = "gemini-flash-2.0", temperature: float = 0.7):
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GOOGLE_API_KEY,
            model=model,
            temperature=temperature
        )

class GroqProvider(BaseLLMProvider):
    def get_llm(self, model: str = "qwen-qwq-32b", temperature: float = 0.7):
        return ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name=model,
            temperature=temperature
        )