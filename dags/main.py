from airflow import DAG
from datetime import datetime
from ..get_data import get_data
from airflow.operators.python import PythonOperator

with DAG("Stock_Data",start_date=datetime(2025,5,31),schedule_interval='0 21 * * 1,3,5',catchup=False) as dag:
    get_raw_data = PythonOperator(task_id="get_stock_data",python_callable=get_data)
    get_raw_data