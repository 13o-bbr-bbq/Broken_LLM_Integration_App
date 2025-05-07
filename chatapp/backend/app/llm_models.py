from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama

from .settings import settings


# Create ChatGPT model for chat.
def create_chat_openai_model():
    provider = settings.LLM_PROVIDER.lower()
    if provider == "openai":
        return ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.OPENAI_MODEL_NAME,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=settings.OPENAI_TEMPERATURE,
            verbose=settings.OPENAI_VERBOSE
        )
    elif provider == "ollama":
        return Ollama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL_NAME,
            verbose=settings.OLLAMA_VERBOSE
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
