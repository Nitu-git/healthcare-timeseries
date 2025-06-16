# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.utils.dates import days_ago
# from datetime import timedelta

# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=1),
# }

# dag = DAG(
#     'clean_and_load_pipeline',
#     default_args=default_args,
#     description='Create tables, clean CSVs and load into Postgres',
#     schedule_interval='@daily',
#     start_date=days_ago(1),
#     catchup=False,
# )

# # Step 1: Create tables if not exists
# create_tables = PostgresOperator(
#     task_id='create_tables',
#     postgres_conn_id='postgres_default',
#     sql='sql/create_tables.sql',
#     dag=dag,
# )

# # Step 2: Clean CSVs with Python script
# clean_csvs = BashOperator(
#     task_id='clean_csvs',
#     bash_command='python /opt/airflow/scripts/clean/clean_csvs.py',
#     dag=dag,
# )

# # Step 3: Load cleaned CSVs into Postgres
# load_data = PostgresOperator(
#     task_id='load_cleaned_data',
#     postgres_conn_id='postgres_default',
#     sql='sql/load_data.sql',
#     dag=dag,
# )

# create_tables >> clean_csvs >> load_data


from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='clean_and_load_pipeline',
    default_args=default_args,
    description='Clean CSVs and load them into Postgres',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    template_searchpath=['/opt/airflow/sql'],  # SQL templates from here
) as dag:

    # Step 1: Clean CSVs with Python script
    clean_csvs = BashOperator(
        task_id='clean_csvs',
        bash_command='python /opt/airflow/scripts/clean/clean_csvs.py',
    )

    # Step 2: Load cleaned CSVs into Postgres
    load_data = PostgresOperator(
        task_id='load_cleaned_data',
        postgres_conn_id='postgres_default',
        sql='load_data.sql',  # Only the filename; path handled by searchpath
    )

    clean_csvs >> load_data
