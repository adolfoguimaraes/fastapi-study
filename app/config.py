
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRES: int
    MONGO_URI: str
    MONGO_DB: str

    class Config:   
        env_file = '.env'


settings = Settings()   