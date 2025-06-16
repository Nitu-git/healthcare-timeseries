from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Make 'scripts/' importable inside container
sys.path.append('/opt/airflow/scripts')

from modeling.train_xgboost import train_xgboost

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='train_xgboost_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 6, 1),
    schedule_interval=None,  # Manual trigger
    catchup=False
) as dag:

    xgboost_task = PythonOperator(
        task_id='train_xgboost',
        python_callable=train_xgboost
    )
