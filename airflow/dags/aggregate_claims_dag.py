from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='aggregate_claims_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',  # or '@once' for dev
    catchup=False,
    template_searchpath=['/opt/airflow/sql'],  
    tags=['claims', 'aggregation', 'forecasting'],
) as dag:

    aggregate_claims = PostgresOperator(
        task_id='aggregate_claims',
        postgres_conn_id='postgres_default',
        sql='aggregate_claims.sql', 
    )

    aggregate_claims
