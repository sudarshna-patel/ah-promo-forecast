import yaml
import numpy as np
import pandas as pd
from src.data_prep.data_loader import load_dataset

## Load parameters from param.yaml
params=yaml.safe_load(open("configs/params.yaml"))['preprocess']

# from dotenv import load_dotenv
# load_dotenv(override=True)
# api_key = os.getenv('OPENAI_API_KEY')

def preprocess():
    df_prep = load_dataset(path=params["input"])
    # df_prep.head(5)

    # Log transform the target column!
    df_prep['UnitSales'] = np.log(df_prep['UnitSales'])

    # convert the column DateKey (string) to a date column
    df_prep['DateKey'] = pd.to_datetime(df_prep['DateKey'], format='%Y%m%d')
    df_prep['month'] = df_prep['DateKey'].dt.month
    df_prep['weekday'] = df_prep['DateKey'].dt.weekday

    # Drop null values
    df_prep_clean_0 = df_prep[df_prep['UnitSales'].notnull()].copy()
    df_prep_clean = df_prep_clean_0[df_prep_clean_0['ShelfCapacity'].notnull()].copy()

    # Convert columns to correct format
    df_prep_clean['month'] = df_prep_clean['month'].astype('category')
    df_prep_clean['weekday'] = df_prep_clean['weekday'].astype('category')

    # df_prep.head()
    return df_prep_clean
