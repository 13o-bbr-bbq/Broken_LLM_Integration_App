from pydantic_settings import BaseSettings


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


    # Setting.
class Settings(Config):
    # MySQL.
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    @property
    def DB_DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    # ChatGPT.
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str
    OPENAI_MAX_TOKENS: int
    OPENAI_TEMPERATURE: float
    OPENAI_VERBOSE: bool


settings = Settings()
