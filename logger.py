import logging
import os

LOG_FILE = "app.log"


def get_logger(name: str):
    logger = logging.getLogger(name)

    # Prevent adding handlers multiple times (VERY IMPORTANT)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Formatter (standard production format)
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    # File handler → writes logs to app.log
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console handler → prints logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent logs from being duplicated by root logger
    logger.propagate = False

    return logger
