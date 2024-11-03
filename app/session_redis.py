import redis
from config import settings
from datetime import datetime

class SessionRedis:
    def __init__(self):
        self.__redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def create_session(self, user_id):
        session_data = {
            'user_id': user_id, 
            "last_access": datetime.now(datetime.timezone.utc).isoformat(), 
            "expire_time": settings.SESSiION_EXPIRE_TIME
        }

        self.__redis.hmset(f"session:{user_id}", session_data)
        self.__redis.expire(f"session:{user_id}", settings.SESSiION_EXPIRE_TIME)