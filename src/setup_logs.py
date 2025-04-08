import os
import logging
from datetime import datetime


def configure_logs(file_name):
    # Set up log path
    log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), file_name)

    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Configure logging
    logging.basicConfig(
        filename=log_path,
        filemode="a",  # Append mode
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # Optional: also print logs to stdout (useful for Docker log viewing)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


# # Begin training
# def train_model():
#     logging.info("Starting training process...")

#     # Simulated steps
#     try:
#         logging.info("Loading data...")
#         # your code here

#         logging.info("Training model...")
#         # your code here

#         logging.info("Saving model...")
#         # your code here

#         logging.info("Training completed successfully!")

#     except Exception as e:
#         logging.exception(f"Training failed due to: {e}")


# # Only run if this is the main file
# if __name__ == "__main__":
#     train_model()
