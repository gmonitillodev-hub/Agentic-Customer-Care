import logging
from pathlib import Path

LOG_DIR = Path("log")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_agent_logger(enable_console=False) -> logging.Logger:
    logger = logging.getLogger("cc_agent_logger")
    logger.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler(LOG_DIR / "error_cc_agent_logger.log")
    error_file_handler.setLevel(logging.ERROR)

    info_file_handler = logging.FileHandler(LOG_DIR / "info_cc_agent_logger.log")
    info_file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formator = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_file_handler.setFormatter(formator)
    info_file_handler.setFormatter(formator)
    console_handler.setFormatter(logging.Formatter('\n %(asctime)s - %(levelname)s - %(message)s \n'))

    logger.addHandler(error_file_handler)
    logger.addHandler(info_file_handler)

    if enable_console:
        logger.addHandler(console_handler)

    return logger

def setup_rag_logger(enable_console=False) -> logging.Logger:
    logger = logging.getLogger("rag_logger")
    logger.setLevel(logging.DEBUG)

    error_file_handler = logging.FileHandler(LOG_DIR / "error_rag_logger.log")
    error_file_handler.setLevel(logging.ERROR)

    info_file_handler = logging.FileHandler(LOG_DIR / "info_rag_logger.log")
    info_file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formator = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_file_handler.setFormatter(formator)
    info_file_handler.setFormatter(formator)
    console_handler.setFormatter(logging.Formatter('\n %(asctime)s - %(levelname)s - %(message)s \n'))

    logger.addHandler(error_file_handler)
    logger.addHandler(info_file_handler)

    if enable_console:
        logger.addHandler(console_handler)

    return logger