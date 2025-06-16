from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
# Add scripts to sys.path so Airflow can find your module
sys.path.append('/opt/airflow/scripts')

# Import from scripts/evaluation/evaluate_models.py
from evaluation.export_claims_vs_forecasts import export_claims_vs_forecasts

with DAG(
    dag_id="evaluate_claims_vs_forecasts_pipeline",
    start_date=datetime(2025, 6, 1),
    schedule_interval=None,
    catchup=False,
    tags=["evaluation", "powerbi"],
) as dag:
    
    export_task = PythonOperator(
        task_id="export_claims_vs_forecasts",
        python_callable=export_claims_vs_forecasts
    )