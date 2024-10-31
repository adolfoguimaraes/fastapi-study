from datetime import timedelta, datetime, timezone
from app.config import settings

from pydantic import BaseModel

from jwt import decode, encode

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    user_id: int | None = None
    role: str | None = None

class UserInfo(BaseModel):
    username: str
    id: int
    role: str


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    
    encode_info = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode_jwt = encode(encode_info, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encode_jwt

def validate_token(token, credentials_exception):
    payload = decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    username: str = payload.get('sub')
    id = payload.get('id')
    role = payload.get('role')
    if not username:
        raise credentials_exception  
    token_data = TokenData(username=username, user_id=id, role=role)
    return token_data