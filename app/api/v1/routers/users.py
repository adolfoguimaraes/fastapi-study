from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError

from app.security import validate_token
from app.security import TokenData

from http import HTTPStatus


router = APIRouter()

@router.get('/', status_code=HTTPStatus.OK)
def index(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()), response_model=TokenData
):
    
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = validate_token(token, credentials_exception)
    except DecodeError:
        raise credentials_exception  


    return token_data
