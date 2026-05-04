from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_aws import ChatBedrockConverse
from langchain_google_genai import ChatGoogleGenerativeAI

from .settings import settings


# Create ChatGPT model for chat.
def create_chat_openai_model():
    provider = settings.LLM_PROVIDER.lower()
    if provider == "openai":
        return ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL or None,
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
    elif provider == "bedrock":
        bedrock_kwargs = dict(
            model=settings.BEDROCK_MODEL_ID,
            max_tokens=settings.BEDROCK_MAX_TOKENS,
            temperature=settings.BEDROCK_TEMPERATURE,
            verbose=settings.BEDROCK_VERBOSE,
        )
        if settings.BEDROCK_REGION_NAME:
            bedrock_kwargs["region_name"] = settings.BEDROCK_REGION_NAME
        if settings.BEDROCK_AWS_ACCESS_KEY_ID:
            bedrock_kwargs["aws_access_key_id"] = settings.BEDROCK_AWS_ACCESS_KEY_ID
        if settings.BEDROCK_AWS_SECRET_ACCESS_KEY:
            bedrock_kwargs["aws_secret_access_key"] = settings.BEDROCK_AWS_SECRET_ACCESS_KEY
        if settings.BEDROCK_AWS_SESSION_TOKEN:
            bedrock_kwargs["aws_session_token"] = settings.BEDROCK_AWS_SESSION_TOKEN
        return ChatBedrockConverse(**bedrock_kwargs)
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            google_api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL_NAME,
            max_output_tokens=settings.GEMINI_MAX_TOKENS,
            temperature=settings.GEMINI_TEMPERATURE,
            verbose=settings.GEMINI_VERBOSE,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
