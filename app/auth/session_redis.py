
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

        self.__redis.hmset(f"session:{session_data['session_id']}", session_data)
        self.__redis.expire(f"session:{session_data['session_id']}", int(settings.REDIS_DELETE_SECONDS))

        return session_data

    def get_connection(self):
        return self.__redis
    
    def get_session(self, session_id):
        return self.__redis.hgetall(f"session:{session_id}")

session_redis = SessionRedis()