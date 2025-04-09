import logging
import os
import sys
from datetime import datetime


def configure_logs(file_name="app.log"):
    log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), file_name)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Create file if it doesn't exist
    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("init")

    # Remove existing handlers (optional, to avoid duplicates)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up file handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Set up console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Apply handlers to root logger
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
