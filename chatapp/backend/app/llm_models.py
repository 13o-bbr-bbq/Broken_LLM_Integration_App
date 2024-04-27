from langchain.chat_models import ChatOpenAI

from .settings import settings


# Create ChatGPT model for chat.
def create_chat_openai_model():
    llm = ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name=settings.OPENAI_MODEL_NAME,
        max_tokens=settings.OPENAI_MAX_TOKENS,
        temperature=settings.OPENAI_TEMPERATURE,
        verbose=settings.OPENAI_VERBOSE
    )
    return llm
