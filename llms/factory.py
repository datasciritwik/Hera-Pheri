from typing import Dict, Type
from llms.providers import BaseLLMProvider, OpenAIProvider, AnthropicProvider, GoogleProvider, GroqProvider

class LLMFactory:
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "groq": GroqProvider
    }
    
    @classmethod
    def create_llm(cls, provider: str, model: str = None, temperature: float = 0.7):
        if provider not in cls._providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls._providers.keys())}")
        
        provider_class = cls._providers[provider]
        provider_instance = provider_class()
        if model is not None:
            return provider_instance.get_llm(model, temperature)
        else:
            return provider_instance.get_llm(temperature=temperature)
    
    @classmethod
    def get_available_providers(cls) -> list:
        return list(cls._providers.keys())