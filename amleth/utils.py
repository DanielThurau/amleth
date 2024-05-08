import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(config):
    """
    Set up the logging configuration for the application.
    Logs will be written to both the console and a rotating file.
    """

    # Convert log level to logging constants
    log_level = config.get("LOG_LEVEL")
    numeric_level = getattr(logging, log_level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    # Ensure the log directory exists
    log_file = config.get("LOG_FILE")
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create handlers (console and file)
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(log_file, maxBytes=1048576, backupCount=5)

    formatter = logging.Formatter(
        "[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def log_starting_message():
    logger = logging.getLogger()
    logger.info(
        """ 
=========================================================================================
      .o.       ooo        ooooo ooooo        oooooooooooo ooooooooooooo ooooo   ooooo 
     .888.      `88.       .888' `888'        `888'     `8 8'   888   `8 `888'   `888' 
    .8"888.      888b     d'888   888          888              888       888     888  
   .8' `888.     8 Y88. .P  888   888          888oooo8         888       888ooooo888  
  .88ooo8888.    8  `888'   888   888          888    "         888       888     888  
 .8'     `888.   8    Y     888   888       o  888       o      888       888     888  
o88o     o8888o o8o        o888o o888ooooood8 o888ooooood8     o888o     o888o   o888o 
=========================================================================================
"""
    )
