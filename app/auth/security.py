from datetime import timedelta, datetime, timezone
import json

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.session_redis import session_redis
from app.config import settings

from pydantic import BaseModel

from jwt import DecodeError, ExpiredSignatureError, decode, encode

from app.exceptions import CredentialException, TokenExpirationException, GeneralException, SessionExpiredException

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

class SessionData(BaseModel):
    session_id: str
    user_id: int
    last_access: float
    expires: float

class UserData(BaseModel):
    username: str
    user_id: int
    role: str
    session_id: str

async def get_current_user(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):

    token_data = validate_token(token)
    session_data = validate_session(token_data.user_id)
    
    user_data = {
        "username": token_data.username,
        "user_id": token_data.user_id,
        "role": token_data.role,
        "session_id": session_data.session_id
    }

    user_data = UserData.model_validate(user_data)

    return user_data


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    expires = datetime.now(timezone.utc) + expires_delta
    encode_info = {"sub": username, "id": user_id, "role": role, "exp": expires}
    
    encode_jwt = encode(encode_info, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encode_jwt

def validate_token(token):
    try:
        payload = decode(token.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get('sub')
        id = payload.get('id')
        role = payload.get('role')
        
        if not username:
            raise CredentialException  
        
        token_data = TokenData(username=username, user_id=id, role=role)

        return token_data
    
    except DecodeError:
        raise CredentialException
    except ExpiredSignatureError:
        raise TokenExpirationException
    except Exception as e:
        print(e)
        raise GeneralException
    
def validate_session(user_id: str):
    session = session_redis.get_session(user_id)

    if not session or len(session) == 0:
        raise SessionExpiredException
   
    session = {
        "session_id": session.get(b"session_id").decode(),
        "user_id": int(session.get(b"user_id").decode()),  
        "last_access": float(session.get(b"last_access").decode()),
        "expires": float(session.get(b"expires").decode())
    }


    session_data = SessionData.model_validate(session)
    
    #if session_data.expires < datetime.now(timezone.utc).timestamp():
    #    raise SessionExpiredException
    
    return session_data