
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(override=True)

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRES: int
    MONGO_URI: str
    MONGO_DB: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    SESSION_EXPIRE_SECONDS: int
    SESSION_COKIES_EXPIRE_SECONDS: int
    REDIS_DELETE_SECONDS: int

    class Config:   
        env_file = '.env'

def get_settings() -> Settings:
    return Settings()

settings = get_settings()   