import logging
from logging.handlers import RotatingFileHandler
import os
import sys

LOG_DIR = os.path.join(os.getcwd(),"logs")
os.makedirs(LOG_DIR,exist_ok=True)

def get_logger(name:str = "chamber"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(logging.INFO)
        consoleFormatter = logging.Formatter(
            "\033[96m[%(levelname)s]\033[0m %(message)s"
        )
        console.setFormatter(consoleFormatter)

        fileHandler = RotatingFileHandler(
            os.path.join(LOG_DIR,"chamber.log"),
            maxBytes=5*1024*1024,
            backupCount=5
        )

        fileHandler.setLevel(logging.DEBUG)
        fileFormatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fileHandler.setFormatter(fileFormatter)

        logger.addHandler(console)
        logger.addHandler(fileHandler)
    return logger

if __name__=="__main__":
    log = get_logger()
    log.info("Chamber log initiated")
    log.debug("Debug message example")
    
