from datetime import timedelta, datetime, timezone
from app.config import settings

from fastapi import APIRouter, Depends

from app.security import create_access_token
from app.security import Token, UserInfo


router = APIRouter()


@router.get("/", response_model=Token)
async def login_for_access_token(
    user: UserInfo = Depends()
): 
    token = create_access_token(username=user.username, user_id=user.id, role=user.role, expires_delta=timedelta(minutes=settings.JWT_EXPIRES))

    return {'access_token': token, 'token_type': 'bearer'}

 
