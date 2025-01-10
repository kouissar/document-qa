from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str = "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"
    CHROMA_PERSISTENCE_DIR: str = "./chroma_db"
    MODEL_NAME: str = "llama3-8b-8192"
    
    class Config:
        env_file = ".env"

settings = Settings() 