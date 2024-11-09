

from http import HTTPStatus
from fastapi import HTTPException


CredentialException = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

TokenExpirationException = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)

GeneralException = HTTPException(
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
    detail="Internal Server Error",
)

NotFoundException = HTTPException(
    status_code=HTTPStatus.NOT_FOUND,
    detail="Task not found.",
)

SessionExpiredException = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail="Session has expired",
    headers={"WWW-Authenticate": "Bearer"},
)