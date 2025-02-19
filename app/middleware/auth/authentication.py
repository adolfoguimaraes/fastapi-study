from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from jwt import DecodeError, ExpiredSignatureError, decode

class AuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: str, algorithms: list):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithms = algorithms
        self.security = HTTPBearer()

    async def dispatch(self, request: Request, call_next):
        credentials: HTTPAuthorizationCredentials = await self.security(request)
        if credentials:
            token = credentials.credentials
            try:
                payload = decode(token, self.secret_key, algorithms=self.algorithms)
                request.state.user = payload
            except DecodeError:
                raise HTTPException(status_code=401, detail="Invalid token")
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
        else:
            raise HTTPException(status_code=403, detail="Authorization header missing")

        response = await call_next(request)
        return response