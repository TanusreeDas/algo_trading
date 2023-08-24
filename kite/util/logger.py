from pathlib import Path
import logging

def setup_logger(filename):

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    log_directory = Path("../data/log")
    log_file_path = log_directory.joinpath(filename)

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
