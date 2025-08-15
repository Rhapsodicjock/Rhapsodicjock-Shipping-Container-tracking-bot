from loguru import logger
import os

def setup_logging(log_dir: str = "logs", level: str = "INFO"):
    os.makedirs(log_dir, exist_ok=True)
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=level)  # console
    logger.add(os.path.join(log_dir, "run_{time}.log"), rotation="1 week", retention="4 weeks", level=level)
    return logger
