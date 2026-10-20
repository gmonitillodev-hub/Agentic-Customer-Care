import logging
from pathlib import Path
from typing import Literal

LOG_DIR = Path("log")

LogType = Literal["agent", "tools", "rag"]


def setup_logger(log_type: LogType, enable_console=False) -> logging.Logger:
    """Create a logger writing to log/<log_type>/{info,error}.log."""
    logger = logging.getLogger(f"{log_type}_logger")
    if logger.handlers:
        return logger  # already configured, avoid duplicated handlers

    log_dir = LOG_DIR / log_type
    log_dir.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler(log_dir / "error.log")
    error_file_handler.setLevel(logging.ERROR)

    info_file_handler = logging.FileHandler(log_dir / "info.log")
    info_file_handler.setLevel(logging.DEBUG)

    formator = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_file_handler.setFormatter(formator)
    info_file_handler.setFormatter(formator)

    logger.addHandler(error_file_handler)
    logger.addHandler(info_file_handler)

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('\n %(asctime)s - %(levelname)s - %(message)s \n'))
        logger.addHandler(console_handler)

    return logger
