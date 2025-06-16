from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add scripts to sys.path so Airflow can find your module
sys.path.append('/opt/airflow/scripts')

# Import from scripts/evaluation/evaluate_models.py
from evaluation.evaluate_forecasts import evaluate_models

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='evaluate_models_pipeline',
    default_args=default_args,
    description='Evaluate ARIMA, XGBoost, LSTM models',
    start_date=datetime(2025, 6, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    evaluate_task = PythonOperator(
        task_id='evaluate_models',
        python_callable=evaluate_models
    )
