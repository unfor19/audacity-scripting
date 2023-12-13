import logging
import os


def create_logger(logger_level=os.getenv('AUDACITY_SCRIPTING_LOGGER_LEVEL', 'info')) -> logging.Logger:
    """
    Create a logger with the specified level
    :param level: debug,info,warning,error,critical
    :type level: str
    :return: A logger"""
    # Create a logger
    logger_name = os.getenv('AUDACITY_SCRIPTING_APP_NAME', __name__)

    logger = logging.getLogger(logger_name)
    # Set the level based on the input
    if logger_level.lower() == 'debug':
        logger.setLevel(logging.DEBUG)
    elif logger_level.lower() == 'info':
        logger.setLevel(logging.INFO)
    elif logger_level.lower() == 'warning':
        logger.setLevel(logging.WARNING)
    elif logger_level.lower() == 'error':
        logger.setLevel(logging.ERROR)
    elif logger_level.lower() == 'critical':
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.NOTSET)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logger.level)

    # Create a formatter
    formatter = logging.Formatter(
        f'%(asctime)s - {logger_name} - %(levelname)s - %(message)s')

    # Add the formatter to the console handler
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

    return logger


logger = create_logger()
