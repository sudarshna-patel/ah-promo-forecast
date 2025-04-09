import pandas as pd
from app.schemas import PromoInput
import pickle
import json
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
from src.utils import convert_log_to_units
from src.constants import LOG_PREDICT
from configs.load_configs import config_params

load_dotenv(override=True)


def load_model():
    # model_path = "models/forecasting_model.pkl"

    model_path = os.getenv("MODEL_PATH", "models")
    model_file_path = os.path.join(model_path, config_params["inference"]["model"])
    logging.info(f"model path {model_file_path}")

    model = None
    if os.path.isfile(model_file_path):
        logging.info("model path is present")
        with open(model_file_path, "rb") as f:
            model = pickle.load(f)
        logging.info("Model loaded successfully.")
    else:
        logging.info("Model file not found — skipping load.")
    return model


# LOADED_MODEL = load_model()


def log_prediction(input_data, prediction_output):
    logging.info("log prediction")
    # Set up log directory and file path
    log_dir = os.getenv(
        "LOG_DIR", "/app/logs"
    )  # Environment variable for log directory
    os.makedirs(log_dir, exist_ok=True)  # Create the directory if it doesn't exist
    log_file_path = os.path.join(log_dir, LOG_PREDICT)

    # Ensure the log file exists
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("")  # Create an empty file if it doesn't exist

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": input_data.dict(),
        "prediction": float(prediction_output),
    }

    with open(log_file_path, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")


snake_to_camel_mapping = {
    "store_count": "StoreCount",
    "shelf_capacity": "ShelfCapacity",
    "promo_shelf_capacity": "PromoShelfCapacity",
    "is_promo": "IsPromo",
    "item_number": "ItemNumber",
    "category_code": "CategoryCode",
    "group_code": "GroupCode",
    "month": "month",
    "weekday": "weekday",
    "unit_sales_7": "UnitSales_-7",
    "unit_sales_14": "UnitSales_-14",
    "unit_sales_21": "UnitSales_-21",
}


def make_prediction(input_data: PromoInput) -> float:
    LOADED_MODEL = load_model()
    if LOADED_MODEL is None:
        logging.info("loaded model is None")
        return "NA"
    # def make_prediction() -> float:
    # columns = ['StoreCount', 'ShelfCapacity', 'PromoShelfCapacity', 'IsPromo',
    #             'ItemNumber', 'CategoryCode', 'GroupCode', 'month', 'weekday',
    #             'UnitSales_-7', 'UnitSales_-14', 'UnitSales_-21']

    # custom_example = pd.DataFrame(
    #     data=[
    #         (781, 12602.000, 4922,True, 8646, 7292, 5494, 11, 3, 6.190, 6.217, 6.075),
    #     ],
    #     columns=columns,
    # )
    logging.info(input_data)
    input_df = pd.DataFrame([input_data.dict()])
    # input_df = pd.DataFrame([input_data])
    input_df["item_number"] = input_df["item_number"].astype(int).astype("category")
    input_df["category_code"] = input_df["category_code"].astype(int).astype("category")
    input_df["group_code"] = input_df["group_code"].astype(int).astype("category")
    input_df["month"] = input_df["month"].astype(int).astype("category")
    input_df["weekday"] = input_df["weekday"].astype(int).astype("category")

    input_df.rename(columns=snake_to_camel_mapping, inplace=True)

    pred = LOADED_MODEL.predict(input_df)
    # Log the prediction
    log_prediction(input_data, pred)

    print(float(pred[0]), convert_log_to_units(pred[0]))
    return int(convert_log_to_units(pred[0]))


if __name__ == "__main__":
    make_prediction(
        {
            "store_count": 781,
            "shelf_capacity": 12602.000,
            "promo_shelf_capacity": 4922,
            "is_promo": True,
            "item_number": "8646",
            "category_code": "7292",
            "group_code": "5494",
            "month": "11",
            "weekday": "3",
            "unit_sales_7": 6.190,
            "unit_sales_14": 6.217,
            "unit_sales_21": 6.075,
        }
    )

# # Mapping from original camelCase/column names to snake_case model inputs
# CAMEL_TO_SNAKE_MAP: Dict[str, str] = {
#     "StoreCount": "store_count",
#     "ShelfCapacity": "shelf_capacity",
#     "PromoShelfCapacity": "promo_shelf_capacity",
#     "IsPromo": "is_promo",
#     "ItemNumber": "item_number",
#     "CategoryCode": "category_code",
#     "GroupCode": "group_code",
#     "month": "month",
#     "weekday": "weekday",
#     "UnitSales_-7": "unit_sales_7",
#     "UnitSales_-14": "unit_sales_14",
#     "UnitSales_-21": "unit_sales_21",
#     "UnitSales": "unit_sales",
# }
