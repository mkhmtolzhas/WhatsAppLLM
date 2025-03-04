from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str
    redis_host: str
    redis_port: int

    class Config:
        env_file = ".env"


settings = Settings()
