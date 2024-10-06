import logging
from datetime import datetime
import os

def setup_logging():
    """Configures the logging settings for the application.

    This function sets up the logging system to record logs in a specified format,
    including timestamps, log levels, and other contextual information (such as 
    the filename, line number, and function name). The logs are saved in a file 
    located in the 'logs' directory, with the filename including the current date 
    in the format YYYYMMDD.

    The log level is set to INFO, meaning that all messages at this level and 
    above (WARNING, ERROR, CRITICAL) will be recorded.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d - %(funcName)s] - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    current_date = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join("logs", f"{current_date}_game.log")

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[logging.FileHandler(log_file)]
    )



