import logging
import sys


def configure_logging():
    logging.basicConfig(
        stream=sys.stdout,  # Log to standard output
        level=logging.INFO,  # Logging level
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # Timestamp format
    )
