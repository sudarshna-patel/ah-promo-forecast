from fastapi import FastAPI, Request, Form, BackgroundTasks, Query
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import json
import time
import os
import asyncio
from app.schemas import PromoInput
from src.inference.predict import make_prediction
from src.training.training_async import train_model_async
from src.setup_logs import configure_logs
from src.constants import LOG_ALL, LOG_TRAIN, LOG_PREDICT

configure_logs(file_name=LOG_ALL)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/train")
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
    unit_sales_21: float = Form(...),
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
            unit_sales_21=unit_sales_21,
        )
        # return {"message": f"Promo uplift predictor is running! {input_data}"}
        prediction = make_prediction(input_data)
        return {"message": f"Promo uplift sales value is {prediction}"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/retrain")
async def retrain_model():
    return {"message": "Placeholder Retraining complete."}


# Endpoint to stream the logs
@app.get("/monitor-training")
async def stream_training_logs():
    def iter_log_file():
        log_path = os.path.join(os.getenv("LOG_DIR", "/app/logs"), LOG_TRAIN)
        with open(log_path, "r") as log_file:
            while True:
                line = log_file.readline()
                if not line:
                    break
                yield line

    return StreamingResponse(iter_log_file(), media_type="text/plain")


@app.get("/monitor")
async def monitor_logs(limit: Optional[int] = Query(10, ge=1, le=100)):
    try:
        log_file = os.path.join(os.getenv("LOG_DIR", "/app/logs"), LOG_PREDICT)
        with open(log_file, "r") as f:
            lines = f.readlines()
            # Get last N lines
            recent_logs = lines[-limit:]
            return [json.loads(line) for line in recent_logs]
        # return {
        #     "status": "Placeholder Everything is running smoothly!",
        #     "timestamp": time.time(),
        # }
    except Exception as e:
        return {"error": str(e)}


@app.get("/load-test")
async def load_test():
    return {"status": "Load testing placeholder."}
