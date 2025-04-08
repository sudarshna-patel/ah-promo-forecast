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
CMD ["sh", "-c", "mlflow ui --host 0.0.0.0 --port 5000 & gunicorn --timeout 3600 --workers 2 --worker-class uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --reload"]


#############
# FROM python:3.11-slim

# RUN apt-get update && apt-get install -y bash

# WORKDIR /app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Create the logs and mlruns directories where logs will be stored
# RUN mkdir -p /app/logs
# RUN mkdir -p /app/mlruns
# RUN chmod -R 777 /app

# # Expose necessary ports
# EXPOSE 8000 5000

# # Start Redis and the app in the background
# CMD ["sh", "-c", "mlflow ui --host 0.0.0.0 --port 5000 & uvicorn myapp:app --host 0.0.0.0 --port 8000 --reload"]

####################
# FROM python:3.11-slim

# # Set env variables to reduce cache and noise
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     DEBIAN_FRONTEND=noninteractive

# # Install only needed packages, use --no-install-recommends
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends bash redis-server gcc g++ build-essential && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Set working directory
# WORKDIR /app

# # Install Python dependencies first for caching
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy rest of the code
# COPY . .

# # Prepare logs and model directory
# RUN mkdir -p /app/logs /app/mlruns && \
#     chmod -R 777 /app

# # Expose required ports
# EXPOSE 8000 5000 6379

# # Launch everything (dev mode: consider supervisord for prod)
# CMD ["sh", "-c", "redis-server & celery -A celery_config.celery_app worker --loglevel=info & mlflow ui --host 0.0.0.0 --port 5000 & uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
