from datetime import timedelta, datetime, timezone

from fastapi.security import HTTPAuthorizationCredentials
from app.config import settings

from fastapi import APIRouter, Depends, Response

from app.auth.security import create_access_token, validate_token
from app.auth.security import Token, UserInfo

from app.auth.session_redis import session_redis

from app.middleware.logs.log_middleware import logger

router = APIRouter()


@router.get("/",
    summary="Login for access token.",
    response_description="Token access for authentication.",         
    response_model=Token,
    response_model_by_alias=False)
async def login_for_access_token(
    response: Response,
    user: UserInfo = Depends(),
): 
    """
    Login for access token.

    - `username` is required.
    - `password` is required.
    - `role` is required.
    """
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=settings.JWT_EXPIRES))

    if token:
        token_data = validate_token(HTTPAuthorizationCredentials(scheme='bearer', credentials=token))
        session_data = session_redis.create_session(user_id=token_data.user_id)

        response.set_cookie(
            key='session_id',
            value=session_data['session_id'],
            httponly=True,
            expires=datetime.fromtimestamp(session_data['expires'], tz=timezone.utc)
        )

        logger.getLogger().info(f"user {token_data.user_id} ({token_data.username} - {token_data.role}) authenticated.")
        logger.getLogger().info(f"user {token_data.user_id} - session {session_data['session_id']} created.")

        
    return Token(access_token=token, token_type='bearer')

 
