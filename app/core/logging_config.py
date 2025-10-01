import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Intercepts standard logging messages and redirects them to Loguru.
    """

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level: str):
    """
    Sets up the logging configuration using Loguru.

    This function removes default handlers, configures Loguru to output
    structured JSON logs, and intercepts standard logging messages.

    Args:
        log_level: The minimum log level to output (e.g., "INFO", "DEBUG").
    """
    # Remove any existing handlers
    logger.remove()

    # Add a new handler with JSON format
    logger.add(
        sys.stdout,
        level=log_level.upper(),
        format="{message}",  # Loguru handles the structure
        serialize=True,  # This enables JSON output
        enqueue=True,  # Make logging async-safe
        backtrace=True,  # Show full stack trace on exceptions
        diagnose=True,  # Add exception details
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.info(f"Logging configured with level: {log_level.upper()}")
