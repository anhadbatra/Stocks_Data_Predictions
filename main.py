from airflow import DAG
from datetime import datetime
from get_data import get_raw_data
from transform import transform_data
from linear_regression import get_data
from airflow.operators.python import PythonOperator

with DAG("my_dag",start_date=datetime(2021,1,1),schedule_interval="@daily",catchup=False) as dag:
    get_raw_data = PythonOperator(task_id="raw_data",python_callable=get_raw_data)
    transform_data = PythonOperator(task_id="transform_data",python_callable=transform_data)
    get_data = PythonOperator(task_id="get_data",python_callable=get_data)


    get_raw_data >> transform_data >> get_data