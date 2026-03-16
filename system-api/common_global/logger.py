"""
Docstring for system-api.common_global.logger

Responsibility:
- central logging cofiguration
- provides consistent logger across the application
- avoids duplicating handlers
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from config_loader import load_config

_config = load_config()

def get_logger(name: str) -> logging.Logger:
    """
    Docstring for get_logger
    
    returns a configured logger instance. 

    Argus: 
        name (str): logger name (usually __name__)
    returns: 
        logging.Logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger
    
    logger.setLevel(_get_log_level())

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    #console handler (for local/dev)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    #optional file handler for prod
    if _is_file_logging_enabled():
        file_handler = RotatingFileHandler(
            filename=_config["logging"]["file"]["path"],
            maxBytes=-_config["logging"]["file"]["max_size_mb"] * 1024 * 1024,
            backupCount=_config["logging"]["file"]["backup_count"],
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    logger.propagate = False

    return logger

def _get_log_level() -> int:
    """
    Return log level from config
    """
    level = _config.get("logging", {}).get("level", "INFO").upper()

    return getattr(logging, level, logging.INFO)

def _is_file_logging_enabled() -> bool:
    """
    check if file logging is enabled
    """

    return _config.get("logging", {}).get("file", {}).get("enabled", False)
