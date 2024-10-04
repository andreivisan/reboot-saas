import logging
import sys
from pathlib import Path

def setup_logging(log_file: str = None, log_level: str = "INFO"):
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(level=log_level, format=log_format, stream=sys.stdout)
    
    # Create custom logger
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    return logger

def get_logger(name: str):
    return logging.getLogger(f"app.{name}")
