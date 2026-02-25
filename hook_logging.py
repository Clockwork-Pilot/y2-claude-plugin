"""Centralized logging configuration for hook handlers."""

import logging
import json
from config import HOOKS_LOG_FILE, HOOKS_LOG_LEVEL


def setup_logger(name: str, output=None) -> logging.Logger:
    """
    Set up and return a configured logger instance.

    Args:
        name: Logger name (typically __name__)
        output: Optional output destination - can be a file path (str) or stream object.
                Defaults to HOOKS_LOG_FILE if not provided.

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(getattr(logging, HOOKS_LOG_LEVEL))

    formatter = logging.Formatter('%(message)s')

    if output is None:
        handler = logging.FileHandler(str(HOOKS_LOG_FILE))
    elif isinstance(output, str):
        handler = logging.FileHandler(str(output))
    else:
        handler = logging.StreamHandler(output)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def serialize_log_data(data: dict) -> str:
    """Serialize log data to JSON format."""
    return json.dumps(data)


def deserialize_log_data(json_str: str) -> dict:
    """Deserialize JSON string back to dictionary."""
    return json.loads(json_str)


__all__ = ["setup_logger", "serialize_log_data", "deserialize_log_data"]
