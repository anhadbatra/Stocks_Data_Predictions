from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from sentiment_analysis import sentiment_analysis


with DAG("Sentiment_DAG",start_date=datetime(2025,5,18),schedule_interval='0 15 * * 1-5',catchup=False) as dag:
    run_sentiment = PythonOperator(task_id="sentiment_analysis",python_callable=sentiment_analysis)