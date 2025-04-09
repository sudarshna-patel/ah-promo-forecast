---

# ✨ Personal Note

First of all, let me just say — I absolutely loved working on this project!

---

# 📈 Promo Uplift ML Application

This project contains a machine learning application that predicts sales uplift during promotional campaigns for Albert Heijn. The application is built using **FastAPI** for the web interface, **MLflow** for experiment tracking and model serving, and **Docker** for containerized deployment.

My vision was to build a platform where a user could Train, Predict, See training progress, Retrain the model, Monitor model performance and Load test the model. Additionally, I also wanted to include unit tests and integration tests. And, lastly, I also wanted to deploy it to the cloud using a CI/CD pipeline.  
Since in this task, I'm assuming hyperparameter tuning isn't necessary, it could have been implemented in the training module while tracking via MLflow — allowing the best model to be registered and served.

However, due to the limited time, I decided to mainly focus on **train** and **test**, among many other ideas I envisioned.

---

## 🔍 Assumptions

1. Data is already clean and preprocessed  
2. The provided model is adequate for production – no hyperparameter tuning  
3. Model input/output shape is consistent  
4. No retraining on new data for now – training is manual or on demand  
5. A single machine is sufficient (e.g., local dev, Docker, or lightweight cloud VM)  
6. Inference can be one-off or served via API  
7. Docker compatibility is required  
8. Model artifacts are stored locally  
9. Model to be loaded only once  
10. Read/write paths are relative  
11. No actual CI/CD pipeline implemented, but will be discussed  
12. No need for complex orchestration tools  

---

## 🚀 Features

- **📦 FastAPI web app** for training and inference  
- **🧠 MLflow integration** for experiment tracking, model logging, and serving  
- **🐳 Dockerized deployment** for both the web server and MLflow UI  
- **📡 Train and Predict APIs** with background job support for long-running processes  
- **🧪 Placeholder retraining, monitoring & load testing endpoints**  
- **🗂 Logs and artifacts** managed locally, but architecture ready for production  

---

## 🧱 Architecture Overview

```plaintext
Client --> FastAPI App --> Training Module --> MLflow (local server)
                                 |
                                 --> Saved model (local + MLflow artifact)
                                 --> Inference API
```

In production, this can be extended to:
- Host FastAPI + MLflow on AWS **EC2**  
- Use **S3** for MLflow artifacts and log storage  
- Add **Celery + Redis** for scalable background jobs  
- Use **CloudWatch** or similar for monitoring  
- Use **Locust** or similar for load testing  
- Add load balancers for the web server (based on traffic)

---

## 🧪 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/train` | POST   | Triggers model training in the background |
| `/predict` | POST | Runs inference on new data |
| `/retrain` | GET  | Placeholder for retraining workflow |
| `/monitor-training` | GET | Rudimentary logs viewer for training runs |
| `/monitor-performance` | GET | Placeholder for model performance dashboard, end point performace matrix |
| `/load-test` | GET | Placeholder for performance for load testing |

---

## ⚙️ How to Run

### 1. Clone and Navigate
Download the ZIP file and go to the project directory in your terminal.

### 2. Build and Run Docker
```bash
# docker-compose up --build
podman build -t promo-forecast-app .
```
OR
```bash
# docker-compose up --build
docker build -t promo-forecast-app .
```

### 3. Run the container with memory limit
```bash
podman run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v $(pwd):/app promo-forecast-app
```
OR
```bash
docker run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v $(pwd):/app promo-forecast-app
```

This will:
- Launch the FastAPI server on `http://localhost:8000`
- Launch the MLflow server on `http://localhost:5000`

### 4. Access
- **FastAPI Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)  
- **MLflow UI**: [http://localhost:5000](http://localhost:5000)

---

## 📂 Project Structure

```
project/
│
├── app/
│   ├── templates/          # FastAPI UI             
|   ├── schemas.py          # Schemas
│   └── main.py             # FastAPI app
│
├── configs/                # configs
├── data/                   # data (project level - can be store somewhere permanent and loaded as volume for efficiency)
├── src/                    # Core logic: training, inference
├── mlruns/                 # MLflow experiment tracking (container level - can be store somewhere permanent and loaded as volume)
├── models/                 # Saved model files for serving (container level - can be store somewhere permanent and loaded as volume)
├── logs/                   # contains the logs (container level - can be store somewhere permanent and loaded as volume)
├── tests                   # placeholder for tests
├── Dockerfile
├── run-promo-app.sh        # script to run the project
├── .gitignore              # gitignore
├── .pre-commit-config.yaml # coding stype and linting
├── requirements.txt        # required packages
└── README.md

```
---

## 🛠 Engineering Assumptions & Limitations

- Training is triggered via API and runs **as a background task** to avoid blocking.
- **Celery** was considered for background task management, but due to system limitations, it's not implemented. Instead, `BackgroundTasks` and `gunicorn --timeout 3600` with workers was used.
- ML models are saved **locally and as MLflow artifacts**; in production, these should be stored in **S3 or similar**.
- **Logging** is rudimentary and local. Cloud-based centralized logging (e.g., AWS CloudWatch) is recommended for production.
- The **monitoring and load testing endpoints are placeholders** to show how they could be structured.
- **Unit testing is not included** due to time constraints, but the project is structured for testability.

---

## 🚀 Deployment in Production

Suggested production stack:
- **FastAPI app** hosted on **AWS EC2**
- **MLflow server** also on EC2, or separate instance
- **Model artifacts/logs** stored in **S3**
- **Redis + Celery** for distributed training jobs
- **NGINX/Gunicorn** in front of FastAPI for load handling
- **Monitoring** via Prometheus/Grafana or AWS CloudWatch
- **Locust** for load testing
---

## 📌 To Improve (Given More Time)

- Integrate **Celery + Redis** for proper job queuing
- Add **unit/integration tests** and a CI/CD pipeline
- Expand training logs and metrics dashboards
- Secure MLflow access with basic auth or OAuth
- Better error handling and input validation
- Retraining module implementation

---

## 🙌 Closing Thoughts

I genuinely enjoyed building this project and look forward to walking you through my thought process during the interview.

---