# src/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    mongodb_url: str
    model_name: str = "gpt-3.5-turbo"
    max_tokens: int = 1500
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()