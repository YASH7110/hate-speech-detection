from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Twitter API
    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    TWITTER_ACCESS_TOKEN: str
    TWITTER_ACCESS_SECRET: str
    TWITTER_BEARER_TOKEN: str
    
    # YouTube API
    YOUTUBE_API_KEY: str
    
    # Model Paths
    HATE_SPEECH_MODEL_PATH: str = "trained_models/hate_speech_classifier.pkl"
    VECTORIZER_PATH: str = "trained_models/vectorizer.pkl"
    FASTTEXT_MODEL_PATH: str = "trained_models/lid.176.bin"
    
    # Server Config
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
