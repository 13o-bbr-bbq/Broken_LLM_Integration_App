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

    # Auth (JWT).
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM provider selection.
    LLM_PROVIDER: str = "openai"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL_NAME: str = ""
    OPENAI_MAX_TOKENS: int = 256
    OPENAI_TEMPERATURE: float = 0.9
    OPENAI_VERBOSE: bool = False
    OLLAMA_BASE_URL: str = ""
    OLLAMA_MODEL_NAME: str = ""
    OLLAMA_VERBOSE: bool = False

    # Amazon Bedrock (IAM auth).
    BEDROCK_REGION_NAME: str = ""
    BEDROCK_MODEL_ID: str = ""
    BEDROCK_AWS_ACCESS_KEY_ID: str = ""
    BEDROCK_AWS_SECRET_ACCESS_KEY: str = ""
    BEDROCK_AWS_SESSION_TOKEN: str = ""
    BEDROCK_MAX_TOKENS: int = 256
    BEDROCK_TEMPERATURE: float = 0.9
    BEDROCK_VERBOSE: bool = False

    # Google Gemini.
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = ""
    GEMINI_MAX_TOKENS: int = 256
    GEMINI_TEMPERATURE: float = 0.9
    GEMINI_VERBOSE: bool = False

    # DeepKeep.
    DK_API_URL: str
    DK_FIREWALL_ID: str
    DK_TOKEN: str



settings = Settings()
