import logging
import os

# Change this from "/app/logs/..." to "./logs/..."
LOG_PATH = "./logs/honeypot.log"

def get_logger():
    # This creates the 'logs' folder in your current directory
    os.makedirs("./logs", exist_ok=True)

    logger = logging.getLogger("Honeypot")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Now LOG_PATH points to the directory you just checked/created
        file_handler = logging.FileHandler(LOG_PATH)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger