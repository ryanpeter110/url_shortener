#############
## imports ##
#############


import logging
from logging.handlers import RotatingFileHandler


######################
## class definition ##
######################


class Rotolog:
    """
    a custom logger setup using the rotatingfilehandler for log rotation.
    """

    def __init__(self, log_file_name: str, log_format: str, max_log_files: int = 5, max_log_file_size: int = 1024*1024, log_level: int = logging.DEBUG) -> None:
        """
        initialize the rotolog class.

        args:
            log_file_name (str): the full path of the log file.
            log_format (str): the format of the log messages.
            max_log_files (int): the maximum number of log files that will be created (default is 5).
            max_log_file_size (int): the maximum size of a single log file in bytes (default is 1mb).
            log_level (int): the level of the logs that will be logged (default is debug).
        """
        self.log_file_name = log_file_name
        self.log_format = log_format
        self.max_log_files = max_log_files
        self.max_log_file_size = max_log_file_size
        self.log_level = log_level

        self.setup_logger()
 
    def setup_logger(self) -> None:
        """
        setup the logger with the specified configuration.
        """
        self.logger = logging.getLogger(self.log_file_name)
        self.logger.setLevel(self.log_level)

        file_handler = RotatingFileHandler(
            self.log_file_name,
            maxBytes=self.max_log_file_size,
            backupCount=self.max_log_files
        )

        formatter = logging.Formatter(self.log_format)
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """
        log a debug message.

        args:
            message (str): the message to log.
        """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """
        log an info message.

        args:
            message (str): the message to log.
        """
        self.logger.info(message)
    
    def error(self, message: str) -> None:
        """
        log an error message.

        args:
            message (str): the message to log.
        """
        self.logger.error(message)
