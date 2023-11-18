"""Implements a custom logger with custom levels."""

import logging
import time
from functools import wraps

GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"
GREEN_HIGHLIGHT = "\x1b[6;30;42m"


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for logging messages.

    This formatter is used to color log messages according to their level.

    Attributes:
        format (str): The format string for the log message.
        FORMATS (dict): A dictionary mapping log levels to format strings.
    """

    format = (
        "%(asctime)s - %(name)s - %(levelname)s -",
        " %(message)s (%(filename)s:%(lineno)d)",
    )
    FORMATS = {
        logging.DEBUG: GREY + format + RESET,
        logging.INFO: GREY + format + RESET,
        logging.WARNING: YELLOW + format + RESET,
        logging.ERROR: RED + format + RESET,
        logging.CRITICAL: BOLD_RED + format + RESET,
    }

    def format(self, record):
        """Format the log message."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# ----------------------  Instantiate logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Set custom formatter
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

# ----------------------Define a custom logging method
TIMING = 21
logging.addLevelName(TIMING, "TIMING")


def timing(self, message, *args, **kws):
    """Define logging method for timing."""
    # Color message
    message = GREEN_HIGHLIGHT + "----- TIMING:" + message + RESET
    if self.isEnabledFor(TIMING):
        # Yes, logger takes its '*args' as 'args'.
        self._log(TIMING, message, args, **kws)


logging.Logger.timing = timing


# ----------------------  Define a decorator for timing functions
def timed_function(func):
    """Log function execution time and highlight it.

    Parameters
    ----------
    func : _type_
        Function to be timed.

    Returns
    -------
    _type_
        Decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrap function to be timed."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.timing(
            (
                f"Function {func.__name__} took",
                f" {execution_time:.4f} seconds to run.",
            ),
        )
        return result

    return wrapper
