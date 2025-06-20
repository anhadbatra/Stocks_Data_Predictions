# 📈 Stock Sentiment Forecasting System

An end-to-end machine learning pipeline that predicts stock prices by combining sentiment analysis of unstructured news data with historical stock prices. This system is production-ready with full orchestration, CI/CD, and real-time deployment.

---

## 🚀 Overview

This project integrates data engineering, ML modeling, and MLOps to build a real-time stock forecasting platform using:

- **Apache Airflow** for workflow orchestration  
- **Snowflake** and **dbt** for modern data warehousing and transformations  
- **LSTM** model for time-series forecasting  
- **Docker**, **Jenkins**, and **Kubernetes** for CI/CD and scalable deployment  
- **FastAPI** for serving real-time predictions

---

## 🔧 Tech Stack

| Layer           | Tools Used                                        |
|----------------|---------------------------------------------------|
| Ingestion       | BeautifulSoup, Financial APIs, Python scripts     |
| Sentiment       | VADER, TextBlob                                   |
| Data Storage    | Snowflake (Sentiment & Stock Datamarts)           |
| Transformation  | dbt                                               |
| Orchestration   | Apache Airflow                                    |
| Modeling        | TensorFlow, LSTM                                  |
| CI/CD           | Jenkins, Docker                                   |
| Deployment      | Kubernetes, FastAPI                               |

---

## 📂 Project Structure
app - Model File and FastAPI File
dags - Airflow DAGS file for orchistration 
images - Images of Project
fact_table_stocks - DBT files
K8 - Kubenetes Files
Dockerfile 

## 🧪 How It Works

### 1. Data Ingestion
- Scrape financial news articles with `BeautifulSoup`
- Pull historical stock prices via financial APIs

### 2. Sentiment Analysis
- Use `VADER` and `TextBlob` to analyze article sentiment
- Store scores in Snowflake **Sentiment Datamart**

### 3. Data Transformation
- Load raw stock and sentiment data into Snowflake
- Clean and join using **dbt**, resulting in a unified fact table

### 4. Workflow Orchestration
- Create Airflow DAGs to schedule and trigger:
  - Scraping jobs
  - Stock data updates
  - dbt models
  - Model training (optional)

### 5. Modeling
- Train `LSTM` on the merged dataset
- Save model and evaluate (achieved **MSE = 1.2**)

### 6. Deployment & CI/CD
- Dockerize FastAPI + model
- Jenkins pipeline:
  - Builds Docker image  
  - Pushes to Docker Hub  
  - Applies Kubernetes manifests for deployment

### 7. API Interface
- `FastAPI` exposes prediction endpoint:
  - `POST /predict` → returns predicted stock price


⚙️ Setup Instructions

Apply the credentials for the .env file in the root directory as well as 
1. Clone the Repo

git clone https://github.com/yourusername/stock-ml-pipeline.git
cd stock-ml-pipeline
2. Install Requirements

pip install -r requirements.txt
3. Configure Airflow

export AIRFLOW_HOME=./<your airflow directory>
airflow db init
airflow webserver --port 8080

4. Train Model Locally
python model/train.py

5. Run FastAPI Locally
uvicorn app.main:app --reload

6. Docker & Kubernetes Deployment
# Build and push image
docker build -t yourdockerhub/stock-predictor:latest .
docker push yourdockerhub/stock-predictor:latest

# Apply to cluster
kubectl apply -f kubernetes/

📈 Results
Model: LSTM with 4 past timesteps + sentiment input

Evaluation Metric: MSE = 1.2 on validation set

API Latency: ~150ms average response time

🤝 Contributing
Pull requests welcome! For major changes, please open an issue first to discuss your idea.

## 🧪 Live API Test (Kubernetes Deployment)

Below is a successful `curl` request to the deployed model endpoint on Kubernetes using Minikube:

![Alt text](https://github.com/anhadbatra/Stocks_Data_Predictions/blob/main/images/Screenshot%202025-06-19%20230335.png)
