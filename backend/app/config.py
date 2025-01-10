from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    CHROMA_PERSISTENCE_DIR: str = "./chroma_db"
    MODEL_NAME: str = "mixtral-8x7b-32768"
    
    class Config:
        env_file = ".env"

settings = Settings() 