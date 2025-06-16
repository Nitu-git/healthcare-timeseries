from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
from airflow.utils.dates import days_ago

sys.path.append('/opt/airflow/scripts')

from modeling.split_train_test import split_train_test

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='split_train_test_pipeline',
    default_args=default_args,
    description='Split engineered features into train/test sets',
    schedule_interval=None,  # Manual trigger
    start_date = days_ago(1),
    catchup=False,
    tags=['claims', 'modeling']
) as dag:

    split_data = PythonOperator(
        task_id='split_train_test',
        python_callable=split_train_test
    )
