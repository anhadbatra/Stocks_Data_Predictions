from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2025, 6, 10),
    'retries': 1,
}

with DAG('dbt_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /path/to/your/dbt/project && dbt run',
    )


    dbt_run 