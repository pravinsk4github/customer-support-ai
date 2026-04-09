import logging
from logging import Filter, LogRecord

from app.core.request_context import get_request_id

class RequestIdFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        record.request_id = get_request_id()
        return True

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s | %(message)s"
        )
        handler.setFormatter(formatter)
        handler.addFilter(RequestIdFilter())

        logger.addHandler(handler)
        logger.propagate = False
    
    return logger

