from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import sys
import os

# Make sure scripts/ is importable inside the container
sys.path.append('/opt/airflow')  # matches volume mount in docker-compose

from scripts.features.generate_claims_features import generate_claims_features

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='generate_claims_features_pipeline',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@daily',  # or use '@once' during development
    catchup=False,
    tags=['features', 'claims'],
) as dag:

    generate_features = PythonOperator(
        task_id='generate_claims_features',
        python_callable=generate_claims_features
    )

    generate_features
