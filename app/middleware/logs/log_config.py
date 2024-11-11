LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(session_id)s - %(message)s",
        },
        "uvicorn": {
            "format": "%(asctime)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "uvicorn": {
            "class": "logging.StreamHandler",
            "formatter": "uvicorn",
        },
        "uvicorn_file": {
            "formatter": "uvicorn",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filename": "./logs/server.log",
            "when": "midnight",
            "encoding": "utf8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filename": "./logs/app.log",
            "when": "midnight",
            "encoding": "utf8",
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["uvicorn","uvicorn_file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["uvicorn","uvicorn_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["uvicorn","uvicorn_file"],
            "level": "INFO",
            "propagate": False,
        },
      
    },
}