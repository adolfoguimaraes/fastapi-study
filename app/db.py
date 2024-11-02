from typing import Annotated

from pydantic import BeforeValidator
from app.config import settings

from motor.motor_asyncio import AsyncIOMotorClient




class DatabaseConnection:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]

    
    async def close(self):
        self.client.close()


db_connection = DatabaseConnection()
