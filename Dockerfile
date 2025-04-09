FROM python:3.11-slim

RUN apt-get update && apt-get install -y bash

WORKDIR /app

COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the logs and mlruns directories where logs will be stored
RUN mkdir -p /app/logs && mkdir -p /app/mlruns && mkdir -p /app/models && chmod -R 777 /app

# Expose necessary ports
EXPOSE 8000 5000

# Start MLflow UI and Gunicorn with specified timeout in the background
CMD ["sh", "-c", "mlflow ui --host 0.0.0.0 --port 5000 & gunicorn --timeout 3600 --workers 2 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --log-level info --access-logfile - --error-logfile -"]
# CMD ["sh", "-c", "mlflow ui --host 0.0.0.0 --port 5000 & gunicorn --timeout 3600 --workers 2 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --reload --log-level info --access-logfile - --error-logfile -"]