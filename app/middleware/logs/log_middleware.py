
from fastapi import Request
import logging
from .log_config import LOGGING_CONFIG
from starlette.middleware.base import BaseHTTPMiddleware

class LoggerMiddleware:
    def __init__(self, app):
        logging.config.dictConfig(LOGGING_CONFIG)
        self.__logger = logging.getLogger("app_logger")
        self.__app = app

        self.__app.add_middleware(BaseHTTPMiddleware, dispatch=self.log_middleware)


    async def log_middleware(self, request: Request, call_next):

        log_dict = {
            "method": request.method,
            "path": request.url.path,
            "query_params": request.query_params,
        }

        self.__logger.info(log_dict)

        response = await call_next(request)

        return response

