import pandas as pd
import logging


def load_dataset(path: str) -> pd.DataFrame:
    logging.info(f"Reading file from {path}")
    return pd.read_csv(path, sep=";", header=0)
