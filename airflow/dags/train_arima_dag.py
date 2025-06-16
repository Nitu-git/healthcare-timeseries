from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/scripts')

from modeling.train_arima import train_arima


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='train_arima_pipeline',
    default_args=default_args,
    start_date=datetime(2025, 6, 1),
    schedule_interval=None,  # Manual trigger only
    catchup=False
) as dag:

    forecast_task = PythonOperator(
        task_id='train_arima',
        python_callable=train_arima
    )
