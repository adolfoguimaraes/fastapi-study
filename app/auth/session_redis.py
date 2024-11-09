
import redis
from app.config import settings
from datetime import datetime, timedelta, timezone
import uuid

class SessionRedis:
    def __init__(self):
        self.__redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def create_session(self, user_id):

        session_data = {
            "session_id": str(uuid.uuid4()),
            'user_id': user_id, 
            "last_access": datetime.now(timezone.utc).timestamp(), 
            "expires": (datetime.now(timezone.utc) + timedelta(seconds=settings.SESSION_EXPIRE_SECONDS)).timestamp()
        }

        self.__redis.hmset(f"session:{user_id}", session_data)
        self.__redis.expire(f"session:{user_id}", int(settings.SESSION_EXPIRE_SECONDS))

    def get_connection(self):
        return self.__redis
    
    def get_session(self, user_id):
        return self.__redis.hgetall(f"session:{user_id}")

session_redis = SessionRedis()