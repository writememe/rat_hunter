"""
Shared settings file to centrally define variables/settings
"""
# Import modules
import logging
import os
from os import path
import pathlib as pl
from dateutil import tz
from datetime import datetime
import time

# Get path of the current directory under which the settings folder is created
SETTINGS_DIRNAME = os.path.dirname(__file__)
"""
Code block to define various directories used throughout the codebase
"""
REPO_ROOT_DIR = path.abspath(os.path.join(SETTINGS_DIRNAME, "..", ".."))
LOG_DIR = path.abspath(os.path.join(REPO_ROOT_DIR, "logs"))
OUTPUT_DIR = path.abspath(os.path.join(REPO_ROOT_DIR, "outputs"))
RESULT_DIR = path.abspath(os.path.join(REPO_ROOT_DIR, "results"))
DATA_OUTPUT_DIR = path.abspath(os.path.join(OUTPUT_DIR, "data"))
pl.Path(LOG_DIR).mkdir(exist_ok=True, parents=True)
pl.Path(OUTPUT_DIR).mkdir(exist_ok=True, parents=True)
pl.Path(RESULT_DIR).mkdir(exist_ok=True, parents=True)
pl.Path(DATA_OUTPUT_DIR).mkdir(exist_ok=True, parents=True)
CRED_DIR = path.abspath(os.path.join(REPO_ROOT_DIR, "rat_hunter", "backend", "creds"))
# Specify the default location to find your credentials file for python-dotenv
DEFAULT_CRED_ENV = path.abspath(os.path.join(CRED_DIR, ".env"))
"""
Set some timezone defaults
"""
LOCAL_TZ = tz.tzlocal()
TIMESTAMP = now = datetime.now(LOCAL_TZ)
NOW = datetime.utcfromtimestamp(time.time())
LOCAL_TZ_NAME = LOCAL_TZ.tzname(NOW)


class Logger:
    def __init__(
        self,
        log_level: str = "INFO",
        log_name: str = "rat_hunter.log",
        app_name: str = "rat_hunter",
    ):

        # Create a logger object with the app name
        logger = logging.getLogger(app_name)
        # Setup the logging formatters for log and stream outputs
        log_fmt = logging.Formatter("%(asctime)s - " "%(levelname)s - " "%(message)s")
        stream_fmt = logging.Formatter("%(levelname)s - " "%(message)s")
        # Setup file handler and use a different log format for output
        f_handler = logging.FileHandler(log_name)
        f_handler.setFormatter(log_fmt)
        # Setup stream handler and use a different log format for output
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(stream_fmt)
        # Create a dictionary of log_level mappings
        logger_map = {
            "INFO": logging.INFO,
            "DEBUG": logging.DEBUG,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        # Set logging level based on the log_level
        # taken from the user using argparse and the log_level dictionary map above
        # NOTE: This will be an integer value
        # https://docs.python.org/3/library/logging.html#logging-levels
        log_integer = logger_map.get(log_level)
        logger.setLevel(level=log_integer)  # type: ignore
        f_handler.setLevel(level=log_integer)  # type: ignore
        s_handler.setLevel(level=log_integer)  # type: ignore
        # Add these handlers to the logger objects
        logger.addHandler(f_handler)
        logger.addHandler(s_handler)
        # Associate the logger instance as an attribute, ready for logging
        self.logger = logger

    """
    Wrapper methods so we can access the log levels directly.
    For example, instead of doing Logger.logger.info, we can do Logger.info instead
    """

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.debug(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)


# Initialise the logger instance
LOGGER = Logger(log_level="INFO", log_name=os.path.join(LOG_DIR, "rat_hunter.log"))
