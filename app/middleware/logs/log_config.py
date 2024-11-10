LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(levelname)s] - %(asctime)s - %(name)s - %(session_id)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "/tmp/applog.log",
            "mode": "a",
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        }
    },
}