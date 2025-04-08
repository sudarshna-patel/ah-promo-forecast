import asyncio
import logging
from src.training.train import train_model

async def train_model_async():
    try:
        await asyncio.to_thread(train_model)
        logging.info("Training finished.")
    except asyncio.TimeoutError:
        logging.error("Training timed out.")
    except Exception as e:
        logging.error(f"Error during training: {e}")


