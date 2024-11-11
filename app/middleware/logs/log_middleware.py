
from fastapi import Request, Response
import logging
from .log_config import LOGGING_CONFIG

from http import HTTPStatus

from contextvars import ContextVar

# Defina uma ContextVar para armazenar o session_id
session_id_var: ContextVar[str] = ContextVar('session_id', default='unknown')

class SessionIDFilter(logging.Filter):
    def filter(self, record):
        # Adiciona o session_id ao record de log
        record.session_id = session_id_var.get()
        return True

class LoggerMiddleware:
    def __init__(self):
        
        logging.config.dictConfig(LOGGING_CONFIG)
        self.__logger = logging.getLogger("app_logger")
        self.__logger.addFilter(SessionIDFilter())
        
        

        
    def getLogger(self):
        return self.__logger

    async def log_middleware(self, request: Request, call_next):


        session_id = request.cookies.get('session_id', 'unknown')
        session_id_var.set(session_id)

        response = await call_next(request)

        log_dict = {
            "method": request.method,
            "path": request.url.path,
            "query_params": request.query_params,
            "session_id": request.cookies.get('session_id'),
            
        }

        
        self.__logger.info(f"{request.method} {request.url.path} : {response.status_code} {HTTPStatus(response.status_code).phrase}", extra=log_dict)

        return response
    
logger = LoggerMiddleware()