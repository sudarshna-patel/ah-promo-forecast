from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import time
import os
import subprocess
import yaml
import asyncio
from app.schemas import PromoInput
from src.inference.predict import make_prediction
from src.training.training_async import train_model_async

import logging
from datetime import datetime

# Set up log path
log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), "train.log")

# Ensure logs directory exists
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_path,
    filemode="a",  # Append mode
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Optional: also print logs to stdout (useful for Docker log viewing)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)





app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/train")
# async def trigger_training():
#     """Trigger training script asynchronously in background."""
#     try:
#         # return {"message": "1. Training has started in background."}
#         # log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), "train.log")
#         # background_tasks.add_task(train_model)  
#         train_model.delay()  # Asynchronous task with Celery
#         return {"message": "Training has started in background."}
#     except Exception as e:
#         return {"error": str(e)}
async def trigger_training(background_tasks: BackgroundTasks):
    """Trigger training script asynchronously in background."""
    try:
        # Timeout for the background task (e.g., 1 hour)
        # await asyncio.wait_for(train_model_async(), timeout=3600)  # 3600 seconds = 1 hour
        background_tasks.add_task(train_model_async)
        return {"message": "Training has started in background."}
    except asyncio.TimeoutError:
        return {"error": "Training took too long and was timed out."}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict")
async def predict(
    store_count: int = Form(...),
    shelf_capacity: float = Form(...),
    promo_shelf_capacity: int = Form(...),
    is_promo: bool = Form(...),
    item_number: str = Form(...),
    category_code: str = Form(...),
    group_code: str = Form(...),
    month: str = Form(...),
    weekday: str = Form(...),
    unit_sales_7: float = Form(...),
    unit_sales_14: float = Form(...),
    unit_sales_21: float = Form(...)
):
    try:
        input_data = PromoInput(
            store_count=store_count,
            shelf_capacity=shelf_capacity,
            promo_shelf_capacity=promo_shelf_capacity,
            is_promo=is_promo,
            item_number=item_number,
            category_code=category_code,
            group_code=group_code,
            month=month,
            weekday=weekday,
            unit_sales_7=unit_sales_7,
            unit_sales_14=unit_sales_14,
            unit_sales_21=unit_sales_21
        )
        # return {"message": f"Promo uplift predictor is running! {input_data}"}
        prediction = make_prediction(input_data)
        print(prediction)
        return {"message": f"Promo uplift sales value is {prediction}"}
    except Exception as e:
        return {"error": str(e)}



@app.post("/retrain")
async def retrain_model():
    return {"message": "Placeholder Retraining complete."}

@app.get("/monitor")
async def monitor_logs():
    return {"status": "Placeholder Everything is running smoothly!", "timestamp": time.time()}

@app.get("/load-test")
async def load_test():
    return {"dummy": "Placeholder Load testing placeholder."}


# Endpoint to stream the logs
@app.get("/monitor-training")
async def stream_training_logs():
    def iter_log_file():
        log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), "train.log")
        with open(log_path, "r") as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    break
                yield line

    return StreamingResponse(iter_log_file(), media_type="text/plain")




# @app.get("/")
# def root():
#     return {"message": "Promo sales predictor is running!"}


# @app.post("/train")
# def trigger_training():
#     """Trigger training script asynchronously in background."""
#     try:
#         ## Load the parameters from params.yaml
#         params = yaml.safe_load(open("configs/params.yaml"))["train"]
#         log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), "train.log")

#         # Run training script in background
#         subprocess.Popen(
#             ["python", "src/training/train.py"],
#             stdout=open(log_path, "a"),
#             stderr=subprocess.STDOUT,
#             cwd=os.getcwd()
#         )

#         return {"message": "Training has started in background."}
#     except Exception as e:
#         return {"error": str(e)}

# # FIXME: should it post if data sent?
# @app.post("/predict", response_model=PromoPrediction)
# def predict(input_data: PromoInput):
#     # return {"message": f"Promo uplift predictor is running! {input_data}"}
#     try:
#         prediction = make_prediction(input_data)
#         return PromoPrediction(predicted_sales=prediction)
#     except Exception as e:
#         return {"error": str(e)}