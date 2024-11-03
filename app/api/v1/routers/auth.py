from datetime import timedelta, datetime, timezone
from app.config import settings

from fastapi import APIRouter, Depends

from app.security import create_access_token
from app.security import Token, UserInfo


router = APIRouter()


@router.get("/",
    summary="Login for access token.",
    response_description="Token access for authentication.",         
    response_model=Token,
    response_model_by_alias=False)
async def login_for_access_token(
    user: UserInfo = Depends()
): 
    """
    Login for access token.

    - `username` is required.
    - `password` is required.
    - `role` is required.
    """
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=settings.JWT_EXPIRES))
    
    return Token(access_token=token, token_type='bearer')

 
