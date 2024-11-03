from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError

from app.security import validate_token
from app.security import TokenData

from http import HTTPStatus

from app.exceptions import CredentialException


router = APIRouter()

@router.get('/', 
    status_code=HTTPStatus.OK,
    summary="Retrieve the current user information",
    response_description="The current user information",
    response_model=TokenData,
    response_model_by_alias=False)
def index(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):

    try:
        token_data = validate_token(token)
    except DecodeError:
        raise CredentialException  


    return token_data
