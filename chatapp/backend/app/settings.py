from pydantic_settings import BaseSettings

# Setting.
class Settings(BaseSettings):
    # MySQL.
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    @property
    def DB_DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # LLM (ChatGPT or LLM on Ollama).
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str
    OPENAI_MAX_TOKENS: int
    OPENAI_TEMPERATURE: float
    OPENAI_VERBOSE: bool
    OLLAMA_BASE_URL: str
    OLLAMA_MODEL_NAME: str
    OLLAMA_VERBOSE: bool

    # DeepKeep.
    DK_API_URL: str
    DK_FIREWALL_ID: str
    DK_TOKEN: str



settings = Settings()
