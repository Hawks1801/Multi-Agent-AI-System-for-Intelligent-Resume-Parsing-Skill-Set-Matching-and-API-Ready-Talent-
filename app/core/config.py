import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Multi-Agent Resume Intelligence")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # SECURITY
    API_KEY: str = os.getenv("API_KEY", "error404-secret-key")
    
    # DATABASE
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db")
    
    # CHROMA
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chromadb")
    
    # REDIS
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
