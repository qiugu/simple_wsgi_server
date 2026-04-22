import logging

from logging.handlers import TimedRotatingFileHandler
from .env import LOG_PATH

def setup_logger():
    logger = logging.getLogger('wsgi app')
    logger.setLevel(logging.DEBUG)
    # logging.handlers.clear()
    
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H-%M-%S")
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    file_handler = TimedRotatingFileHandler(filename=LOG_PATH, when="D", backupCount=7, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()