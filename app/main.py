import logging.config
from fastapi import FastAPI
import logging

from app.api.v1.routers import router as v1_routers

from app.middleware.logs.log_middleware import LoggerMiddleware
#from app.middleware.auth.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings

app = FastAPI(
    title="API Task Manager",
    version="1.0.0",
    contact={
        "name": "Adolfo Guimarães",
        "url": "https://github.com/adolfoguimaraes",
    },
     license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    redoc_url=None,
    openapi_url=None

)

app.add_middleware(BaseHTTPMiddleware, dispatch=LoggerMiddleware().log_middleware)
#app.add_middleware(AuthenticationMiddleware, secret_key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])



app.include_router(v1_routers, prefix="/api/v1") 