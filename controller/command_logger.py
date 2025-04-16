import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("PolicyLogger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("policy_logs.log", maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
